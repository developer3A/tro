import os
import json
import logging
import requests
from dotenv import load_dotenv

from pytoniq import LiteBalancer, WalletV4R2, begin_cell

from config import *

#log maska
def mask_address(address):
    if len(address) <= 8:
        return "****"
    return f"{address[:4]}...{address[-4:]}"

# Payment Monitoring Functions
def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            try:
                state = json.load(f)
                return state.get('last_lt', 0), set(state.get('processed_txs', []))
            except json.JSONDecodeError:
                logger.error("Error reading state file, starting fresh")
    return 0, set()

def save_state(last_lt, processed_txs):
    state = {
        'last_lt': last_lt,
        'processed_txs': list(processed_txs)
    }
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

async def check_payment(memo):
    last_lt, processed_txs = load_state()
    try:
        url = f"{BASE_URL}&from_lt={last_lt if last_lt > 0 else 0}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if not data.get('ok'):
            return False
        transactions = data.get('result', [])
        if not transactions:
            return False
        highest_lt = last_lt
        for tx in sorted(transactions, key=lambda x: x.get('transaction_id', {}).get('lt', 0), reverse=True):
            tx_id = tx.get('transaction_id', {}).get('hash', '')
            tx_lt = int(tx.get('transaction_id', {}).get('lt', '0'))
            if not tx_id or tx_lt == 0 or tx_id in processed_txs:
                continue
            in_msg = tx.get('in_msg', {})
            amount_nanotons = int(in_msg.get('value', '0'))
            amount_ton = amount_nanotons / 1_000_000_000
            comment = in_msg.get('message', '').strip()
            if amount_ton >= BLOCKCHAIN_FEE and comment == memo:
                sender = in_msg.get('source', 'Unknown')
                highest_lt = max(highest_lt, tx_lt)
                processed_txs.add(tx_id)
                save_state(highest_lt, processed_txs)
                return {
                    'tx_id': tx_id,
                    'lt': tx_lt,
                    'amount_ton': amount_ton,
                    'sender': sender,
                    'comment': comment,
                    'timestamp': tx.get('utime', 'N/A')
                }
        save_state(highest_lt, processed_txs)
        return False
    except Exception as e:
        logger.error(f"Error checking payment: {e}")
        return False

async def process_trc_withdrawal(sender, trc_amount, memo):
    try:
        logger.info(f"Initiating TRC withdrawal: {trc_amount} TRC to {mask_address(sender)} (memo: {mask_address(memo)})")
        load_dotenv()
        mnemonic_string = os.getenv('MNEMONIC')
        if not mnemonic_string:
            logger.error("MNEMONIC not found in .env file")
            return False
        mnemonics = mnemonic_string.split()
        provider = LiteBalancer.from_mainnet_config(1)
        await provider.start_up()
        wallet = await WalletV4R2.from_mnemonic(provider=provider, mnemonics=mnemonics)
        USER_ADDRESS = wallet.address
        JETTON_MASTER_ADDRESS = os.getenv('JETTON_MASTER_ADDRESS')
        DESTINATION_ADDRESS = sender
        USER_JETTON_WALLET = (await provider.run_get_method(
            address=JETTON_MASTER_ADDRESS,
            method="get_wallet_address",
            stack=[begin_cell().store_address(USER_ADDRESS).end_cell().begin_parse()]
        ))[0].load_address()
        trc_amount_nano = int(trc_amount * 10**9)
        forward_payload = (begin_cell()
                          .store_uint(0, 32)
                          .store_snake_string("Token Sent Successfully.")
                          .end_cell())
        transfer_cell = (begin_cell()
                        .store_uint(0xf8a7ea5, 32)
                        .store_uint(0, 64)
                        .store_coins(trc_amount_nano)
                        .store_address(DESTINATION_ADDRESS)
                        .store_address(USER_ADDRESS)
                        .store_bit(0)
                        .store_coins(1)
                        .store_bit(1)
                        .store_ref(forward_payload)
                        .end_cell())
        await wallet.transfer(destination=USER_JETTON_WALLET, amount=int(0.05*1e9), body=transfer_cell)
        await provider.close_all()
        logger.info(f"TRC has been transferred to wallet: {mask_address(sender)}")
        return True
    except Exception as e:
        logger.error(f"Error in TRC withdrawal: {e}")
        return False



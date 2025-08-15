from aiogram.fsm.state import State, StatesGroup


# States
class ContactState(StatesGroup):
    waiting_for_message = State()

class LanguageState(StatesGroup):
    waiting_for_language = State()

class WithdrawStates(StatesGroup):
    waiting_for_wallet = State()
    waiting_for_captcha = State()
    waiting_for_amount = State()
    waiting_for_verify = State()

class AddAdState(StatesGroup):
    waiting_for_link = State()
    waiting_for_reward = State()
    waiting_for_limit = State()
    waiting_for_description = State()
    waiting_for_photo = State()

class BroadcastMessage(StatesGroup):
    waiting_for_text = State()

class ReplyState(StatesGroup):
    waiting_for_reply = State()


class GetBaseFilePassword(StatesGroup):
    wait_password = State()


class ReferrerCaptcha(StatesGroup):
    wait_captcha = State()


# class ContactSatte(StatesGroup):
#     wait_message = State()

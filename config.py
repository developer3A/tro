from dotenv import load_dotenv
import logging
import os


# Logging sozlamalari
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# .env faylidan tokenni olish
load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
if not API_TOKEN:
    logger.error("API_TOKEN topilmadi. .env faylida TELEGRAM_BOT_TOKEN ni tekshiring.")
    exit(1)

# Bot konfiguratsiyasi
ADMIN_ID = int(os.getenv('ADMIN_ID'))  # Admin ID from .env or default
PAYMENT_WALLET = os.getenv('PAYMENT_WALLET')  # Default wallet
BLOCKCHAIN_FEE = 0.04
LIMIT = "20"
BASE_URL = f"https://toncenter.com/api/v2/getTransactions?address={PAYMENT_WALLET}&limit={LIMIT}&to_lt=0&archival=false"
STATE_FILE = "deposit_state.json"
DB_PATH = 'tronocoin.db'
REFERRAL_BONUS = 5000


DB_PASSWORD = os.getenv('DB_PASSWORD')
CHANNEL_ID = os.getenv('CHANNEL_ID')


# Til sozlamalari
LANGUAGES = {
    'en': {
        'welcome': "Welcome to Tronocoin Airdrop!\nReferral link: https://t.me/{bot_username}?start={user_id}",
        'main_menu': {
            'profile': "👤 Profile",
            'withdraw': "💸 Withdraw",
            'daily_bonus': "🎁 Daily Bonus",
            'earn': "🎯 Earn",
            'contact': "✉️ Contact",
            'top_users': "🏆 Top users",
            'admin_panel': "👨‍💼 Admin panel"
        },
        'contact_start': "✍️ Write your message. We will respond soon.",
        'contact_received': "✅ Your message has been sent. Please wait for our response.",
        'contact_admin_message': "📥 New message:\n\n👤 User: {user_name} (ID: {user_id})\n💬 Message:\n{message}",
        'reply_prompt': "✏️ Write your response.",
        'reply_sent': "✅ Response sent.",
        'reply_failed': "❌ Response not sent. The user may have blocked the bot.",
        'withdraw_start': "💼 Send your TON wallet address:",
        'cancel': "❌ Cancel",
        'invalid_wallet': "Invalid address. Please try again.",
        'captcha_prompt': "🧠 Captcha: {a} + {b} = ?",
        'invalid_captcha': "❌ Incorrect captcha. Please try again.",
        'captcha_number_only': "🔢 Enter only numbers.",
        'withdraw_amount': "💸 How much Tronocoin ($TRC) would you like to withdraw?",
        'invalid_amount': "❗ Please enter a valid number.",
        'insufficient_balance': "📉 Insufficient balance. You have: {balance} $TRC",
        'not_registered': "🚫 You are not registered. /start",
        'payment_instruction': "🔐 To cover blockchain fees and ensure system stability, send {fee} TON to the following address:\n`{wallet}`\n\n📝 Include the following memo:\n`{memo}`\n\n📌 Note: If the memo is not included, the payment will not be accepted.\n\n✅ After sending the payment, press /verify.",
        'verify_prompt': "Please press /verify after sending the payment.",
        'payment_checking': "⏳ Checking payment...",
        'payment_confirmed': "✅ Payment confirmed!\n💰 Amount: {amount:.4f} TON\n🔗 Transaction ID: {tx_id}...\n⏰ Tokens are being sent...",
        'payment_success': "🎉 Success!\n💰 {amount} TRC tokens have been sent to {wallet}!\n✅ Transaction completed.",
        'payment_failed': "❌ An error occurred!\n💰 {amount} TRC has been refunded to your balance.\n🔄 Please try again.",
        'payment_not_found': "❌ Payment not found!\nPlease ensure you sent the payment correctly and included the correct memo.\n\nMemo: {memo}",
        'daily_bonus_prompt': "<b>🎁 Daily Bonus</b>\n\n⏳ Wait until the following time to claim your bonus:\n🕒 <b>Time left:</b> {time}\n💸 <b>Bonus:</b> 0 $TRC\n\n",
        'daily_bonus_ready': "<b>🎁 Bonus ready!</b>\n\n<b>Time:</b> 00:00:00\n<b>Bonus:</b> 3000 $TRC\n\n🎉 Claim now!",
        'daily_bonus_received': "<b>✅ Bonus received!</b>\n\n<b>+3000 $TRC</b>\n🗓 Next bonus: in 12 hours.",
        'daily_bonus_not_ready': "<b>🎁 Daily Bonus</b>\n\n⏳ Bonus not available yet.\n\n<b>🕒 Time left:</b> {time}\n<b>💰 Bonus:</b> 0 $TRC",
        'top_users': "🏆 Top Users (by balance):\n{users_list}",
        'profile': "{profile_line}\n💰 Balance: {balance:,} $TRC\n👥 Referrals: {ref_count}\n🎁 Daily bonus: {bonus_status}\n\n🔗 Referral link:\n{referral_link}",
        'admin_panel': "👥 Total users: {user_count}\n💰 Total balance: {total_balance} Tronocoin\n\n🏆 Top referrers:\n{top_refs}",
        'broadcast_prompt': "Enter the message you want to send:",
        'broadcast_sent': "Message sent to all users.",
        'ad_start': "1. Send the channel link (e.g., https://t.me/channel_name):",
        'ad_reward': "2. Enter the TRC reward for joining the channel:",
        'ad_limit': "Enter the maximum TRC limit for the channel (number):",
        'ad_description': "3. Write a short description of the channel:",
        'ad_photo': "4. Send a photo for the channel:",
        'ad_placed': "✅ Ad placed:\n\nChannel: {link}\nReward: {reward} TRC\n{description}",
        'ad_notification': "📢 New ad! 💸 Earn {reward} TRC!\n🎯 Check the Earn section.",
        'ad_no_ads': "No ads available.",
        'ad_select': "Select an ad to delete:",
        'ad_deleted': "✅ {link} ad deleted.",
        'ad_stats': "Ad performance statistics:\n{stats}",
        'earn_no_ads': "No new ads available at the moment.",
        'earn_caption': "💸 Earn {reward} $TRC!\n🔗 Channel: {link}\n📜 {description}",
        'earn_limit_reached': "{link} -\nReward limit reached and the advertisement has been removed.",
        'earn_already_received': "{link}\n✅ Reward already received.",
        'earn_not_subscribed': "{link}\n❌ You are not subscribed.",
        'earn_error': "{link}\n❌ Could not check channel: {error}",
        'earn_completed': "Check completed.",
        'invalid_reward': "Reward amount must be greater than 0.",
        'invalid_limit': "Limit amount must be greater than 0.",
        'invalid_number': "Please enter only numbers.",
        'invalid_description': "Please write a description.",
        'language_select': "🌍 Select language:"
    },
    'ru': {
        'welcome': "Добро пожаловать в Tronocoin Airdrop!\nРеферальная ссылка: https://t.me/{bot_username}?start={user_id}",
        'main_menu': {
            'profile': "👤 Профиль",
            'withdraw': "💸 Вывод",
            'daily_bonus': "🎁 Ежедневный бонус",
            'earn': "🎯 Заработать",
            'contact': "✉️ Связаться",
            'top_users': "🏆 Топ пользователей",
            'admin_panel': "👨‍💼 Панель администратора"
        },
        'contact_start': "✍️ Напишите ваше сообщение. Мы ответим в ближайшее время.",
        'contact_received': "✅ Ваше сообщение отправлено. Ожидайте ответа.",
        'contact_admin_message': "📥 Новое сообщение:\n\n👤 Пользователь: {user_name} (ID: {user_id})\n💬 Сообщение:\n{message}",
        'reply_prompt': "✏️ Напишите ваш ответ.",
        'reply_sent': "✅ Ответ отправлен.",
        'reply_failed': "❌ Ответ не отправлен. Пользователь мог заблокировать бота.",
        'withdraw_start': "💼 Отправьте адрес вашего TON кошелька:",
        'cancel': "❌ Отмена",
        'invalid_wallet': "Неверный адрес. Попробуйте снова.",
        'captcha_prompt': "🧠 Капча: {a} + {b} = ?",
        'invalid_captcha': "❌ Неверная капча. Попробуйте снова.",
        'captcha_number_only': "🔢 Вводите только цифры.",
        'withdraw_amount': "💸 Сколько Tronocoin ($TRC) вы хотите вывести?",
        'invalid_amount': "❗ Пожалуйста, введите правильное число.",
        'insufficient_balance': "📉 Недостаточно средств. У вас: {balance} $TRC",
        'not_registered': "🚫 Вы не зарегистрированы.",
        'payment_instruction': "🔐 Для покрытия комиссии блокчейна и стабильности системы отправьте {fee} TON на следующий адрес:\n`{wallet}`\n\n📝 Укажите в комментарии (memo):\n`{memo}`\n\n📌 Примечание: Если memo не указан, платеж не будет принят.\n\n✅ После отправки платежа нажмите /verify.",
        'verify_prompt': "Нажмите /verify после отправки платежа.",
        'payment_checking': "⏳ Проверка платежа...",
        'payment_confirmed': "✅ Платеж подтвержден!\n💰 Сумма: {amount:.4f} TON\n🔗 ID транзакции: {tx_id}...\n⏰ Токены отправляются...",
        'payment_success': "🎉 Успешно!\n💰 {amount} TRC токенов отправлено на {wallet}!\n✅ Транзакция завершена.",
        'payment_failed': "❌ Произошла ошибка!\n💰 {amount} TRC возвращено на ваш баланс.\n🔄 Попробуйте снова.",
        'payment_not_found': "❌ Платеж не найден!\nПожалуйста, убедитесь, что вы правильно отправили платеж и указали правильный memo.\n\nMemo: {memo}",
        'daily_bonus_prompt': "<b>🎁 Ежедневный бонус</b>\n\n⏳ Дождитесь следующего времени, чтобы получить бонус:\n🕒 <b>Оставшееся время:</b> {time}\n💸 <b>Бонус:</b> 0 $TRC\n\n",
        'daily_bonus_ready': "<b>🎁 Бонус готов!</b>\n\n<b>Время:</b> 00:00:00\n<b>Бонус:</b> 3000 $TRC\n\n🎉 Получите сейчас!",
        'daily_bonus_received': "<b>✅ Бонус получен!</b>\n\n<b>+3000 $TRC</b>\n🗓 Следующий бонус: через 12 часов.",
        'daily_bonus_not_ready': "<b>🎁 Ежедневный бонус</b>\n\n⏳ Бонус еще недоступен.\n\n<b>🕒 Оставшееся время:</b> {time}\n<b>💰 Бонус:</b> 0 $TRC",
        'top_users': "🏆 Топ пользователей (по балансу):\n{users_list}",
        'profile': "{profile_line}\n💰 Баланс: {balance:,} $TRC\n👥 Рефералы: {ref_count}\n🎁 Ежедневный бонус: {bonus_status}\n\n🔗 Реферальная ссылка:\n{referral_link}",
        'admin_panel': "👥 Всего пользователей: {user_count}\n💰 Общий баланс: {total_balance} Tronocoin\n\n🏆 Топ рефереров:\n{top_refs}",
        'broadcast_prompt': "Введите сообщение, которое хотите отправить:",
        'broadcast_sent': "Сообщение отправлено всем пользователям.",
        'ad_start': "1. Отправьте ссылку на канал (например: https://t.me/channel_name):",
        'ad_reward': "2. Введите количество TRC за подписку на канал:",
        'ad_limit': "Введите максимальный лимит TRC для канала (число):",
        'ad_description': "3. Напишите краткое описание канала:",
        'ad_photo': "4. Отправьте фото для канала:",
        'ad_placed': "✅ Реклама размещена:\n\nКанал: {link}\nНаграда: {reward} TRC\n{description}",
        'ad_notification': "📢 Новая реклама! 💸 Заработайте {reward} TRC!\n🎯 Проверьте раздел Earn.",
        'ad_no_ads': "Нет доступных объявлений.",
        'ad_select': "Выберите объявление для удаления:",
        'ad_deleted': "✅ {link} объявление удалено.",
        'ad_stats': "Статистика эффективности рекламы:\n{stats}",
        'earn_no_ads': "На данный момент новых объявлений нет.",
        'earn_caption': "💸 Заработайте {reward} $TRC!\n🔗 Канал: {link}\n📜 {description}",
        'earn_limit_reached': "{link}\nЛимит награды достигнут.",
        'earn_already_received': "{link}\n✅ Награда уже получена.",
        'earn_not_subscribed': "{link}\n❌ Вы не подписаны.",
        'earn_error': "{link}\n❌ Не удалось проверить канал: {error}",
        'earn_completed': "Проверка завершена.",
        'invalid_reward': "Сумма награды должна быть больше 0.",
        'invalid_limit': "Сумма лимита должна быть больше 0.",
        'invalid_number': "Пожалуйста, вводите только числа.",
        'invalid_description': "Пожалуйста, напишите описание.",
        'language_select': "🌍 Выберите язык:"
    }

}

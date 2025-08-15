from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from config import *


# Utility Functions
def get_main_keyboard(user_id, language='en'):
    buttons = [
        [KeyboardButton(text=LANGUAGES[language]['main_menu']['profile']), KeyboardButton(text=LANGUAGES[language]['main_menu']['withdraw'])],
        [KeyboardButton(text=LANGUAGES[language]['main_menu']['daily_bonus']), KeyboardButton(text=LANGUAGES[language]['main_menu']['earn'])],
        [KeyboardButton(text=LANGUAGES[language]['main_menu']['contact']), KeyboardButton(text=LANGUAGES[language]['main_menu']['top_users'])],
    ]
    if user_id == ADMIN_ID:
        buttons.append([KeyboardButton(text=LANGUAGES[language]['main_menu']['admin_panel'])])
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def get_earn_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Check", callback_data="check_earn")]])

def get_calm_inline_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🎁 Claim Bonus", callback_data="calm_bonus")]])

def get_cancel_keyboard(language='en'):
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=LANGUAGES[language]['cancel'])]], resize_keyboard=True)

def get_verify_keyboard():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="/verify")]], resize_keyboard=True)

def get_language_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")],
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")]
    ])


def referrer_captcha(referred_by:int):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="✅ I am a human", callback_data=f"referrer_{referred_by}")]])
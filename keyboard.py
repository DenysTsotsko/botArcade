from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

profile_cb = CallbackData('balance', 'name')
kb_main = ReplyKeyboardMarkup(resize_keyboard=True)
kb_main.add(KeyboardButton('Help 🆘'), KeyboardButton('Games 🕹'), KeyboardButton('Profile 👤'))


kb_games = ReplyKeyboardMarkup(resize_keyboard=True)
kb_games.add(KeyboardButton('Dice 🎲'), KeyboardButton('Magic cups ✨'), KeyboardButton('Slots 🎰')).insert(KeyboardButton('Exit ⛔️'))

kb_dice = ReplyKeyboardMarkup(resize_keyboard=True)
kb_dice.add(KeyboardButton('Roll the 🎲'), KeyboardButton('Stop game ⛔'))

# kb_cups = ReplyKeyboardMarkup(resize_keyboard=True)
# kb_cups.add(KeyboardButton('Mix 🔄'), KeyboardButton('Stop game ⛔'))

kb_cups_in = ReplyKeyboardMarkup(resize_keyboard=True)
kb_cups_in.add(KeyboardButton('Mix 🔄'), KeyboardButton('Stop game ⛔'))

kb_cups_game = ReplyKeyboardMarkup(resize_keyboard=True)
kb_cups_game.add(KeyboardButton('1'), KeyboardButton('2'), KeyboardButton('3'))

kb_slot = ReplyKeyboardMarkup(resize_keyboard=True)
kb_slot.add(KeyboardButton('Spin ⭕️'), KeyboardButton('Stop game ⛔'))


def get_cancel_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Cancel 🚫'))

    return kb


def get_sign_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Tap to sign up ☑️'))

    return kb

# def get_balance_ikb() -> InlineKeyboardMarkup:
#     ikb = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton('Check your balance', callback_data='select_profile')],
#         [InlineKeyboardButton('Top up your balance')]
#     ])
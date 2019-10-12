from telegram import ReplyKeyboardMarkup


def get_keyboard():
    general_keyboard = ReplyKeyboardMarkup([
        ['Заметка']
    ], resize_keyboard=True)
    return general_keyboard

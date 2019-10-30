from datetime import datetime
from functools import wraps

from telegram import ChatAction, ReplyKeyboardMarkup


def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context,  *args, **kwargs)

    return command_func


def get_keyboard():
    general_keyboard = ReplyKeyboardMarkup([
        ['Notes']
    ], resize_keyboard=True, one_time_keyboard=True)
    return general_keyboard


def get_note_keyboard():
    note_keyboard = ReplyKeyboardMarkup(
            [
                ['Create note', 'List notes'],
                ['Back']
            ],
            resize_keyboard=True,
            one_time_keyboard=True
            )
    return note_keyboard


def get_note_message(note):
    note_id = '#' + note['note_id']
    caption = note['caption'].join('**')
    text = '-\n' + note['text']

    text_message = '\n'.join([
        note_id,
        caption,
        text
    ])

    return text_message

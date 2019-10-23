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
        ['Заметка']
    ], resize_keyboard=True)
    return general_keyboard


def get_note_keyboard():
    note_keyboard = ReplyKeyboardMarkup(
            [
                [
                    ['Create note'],
                    ['List notes']
                ],
                [
                    ['Back']
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
            )
    return note_keyboard


def get_note_message(note):
    note_id = note['note_id']
    caption = note['caption']
    text = note['text']
    d_modify = datetime.fromtimestamp(note['d_modify']).strftime('%d.%m.%Y %H:%M')
    underline = ''

    for e in range(len(caption)):
        underline = underline + '-'

    text_message = '#{}\n{}\n{}\n{}\n--\n{}'.format(
        note_id,
        caption,
        underline,
        text,
        d_modify
    )

    return text_message

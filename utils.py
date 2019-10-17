from datetime import datetime

from telegram import ReplyKeyboardMarkup


def get_keyboard():
    general_keyboard = ReplyKeyboardMarkup([
        ['Заметка']
    ], resize_keyboard=True)
    return general_keyboard


def get_note_message(note):
    note_id = note['note_id']
    caption = note['caption']
    text = note['text']
    d_modify = datetime.timestamp(note['d_modify'])
    underline = ''

    for e in len(caption):
        underline = underline + '-'

    text_message = '#{}\n{}\n{}\n{}\n--\n{}'.format(note_id, caption, underline, text, d_modify)


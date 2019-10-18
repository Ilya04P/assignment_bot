from telegram import ParseMode, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from db import db, get_or_create_chat, create_note


# Start note converstation
def note_start(update, context):
    update.message.reply_text(
        "Добавь заголовок заметки.",
        reply_markup=ReplyKeyboardRemove()
    )

    return 'NOTE_CAPTION'


def note_caption(update, context):
    caption = update.message.text
    context.user_data['caption'] = caption
    update.message.reply_text(
        'Добавь текст заметки'
    )

    return 'NOTE_TEXT'


def note_text(update, context):
    chat = get_or_create_chat(db, update.effective_chat)
    caption = context.user_data['caption']
    text = update.message.text
    note = create_note(db, chat, caption, text)
    message_text = '''
#{note_id}
*{caption}*
----
{text}
----
{d_modify}'''.format(**note)
    update.message.reply_text(message_text, parse_mode=ParseMode.MARKDOWN)

    return ConversationHandler.END

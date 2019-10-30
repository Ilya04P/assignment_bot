from telegram import ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from db import db, get_or_create_chat, create_note
from utils import get_note_keyboard, get_note_message, send_typing_action


def note_menu(update, context):
    update.message.reply_text('Что мне сделать?', reply_markup=get_note_keyboard())


# Start note converstation
@send_typing_action
def note_start(update, context):
    caption = ' '.join(context.args) # А точно ли нужен заголовок, если это быстрая заметка?
    if caption:
        context.user_data['caption'] = caption
        print(context.user_data['caption'])
        reply_text = update.message.reply_text(
            'Добавь текст заметки...'
        )
        context.user_data['message_id'] = [update.effective_message.message_id]
        context.user_data['message_id'].append(reply_text.message_id)
        return 'NOTE_TEXT'

    reply_text = update.message.reply_text(
        "Добавь заголовок заметки...",
        reply_markup=ReplyKeyboardRemove()
    )
    context.user_data['message_id'] = [update.effective_message.message_id]
    context.user_data['message_id'].append(reply_text.message_id)
    return 'NOTE_CAPTION'


@send_typing_action
def note_caption(update, context):
    context.user_data['message_id'].append(update.effective_message.message_id)
    caption = update.message.text
    context.user_data['caption'] = caption
    reply_text = update.message.reply_text(
        'Добавь текст заметки...'
    )
    context.user_data['message_id'].append(reply_text.message_id)

    return 'NOTE_TEXT'


@send_typing_action
def note_text(update, context):
    context.user_data['message_id'].append(update.effective_message.message_id)
    chat = get_or_create_chat(db, update.effective_chat)
    caption = context.user_data['caption']
    text = update.message.text
    note = create_note(db, chat, caption, text)

    clear_keyboard = ReplyKeyboardMarkup([
        ['Очистить'], ['Оставить']
    ], resize_keyboard=True, one_time_keyboard=True)

    context.bot.send_message(
        chat_id=chat['chat_id'],
        text=get_note_message(note),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=clear_keyboard
    )

    return 'NOTE_CLEAR_CONVERSATION'


@send_typing_action
def note_cancel(update, context):
    if 'message_id' in context.user_data:
        del context.user_data['message_id']

    return ConversationHandler.END


@send_typing_action
def note_clear(update, context):
    context.user_data['message_id'].append(update.effective_message.message_id)
    chat_id = update.effective_chat.id
    for message in context.user_data['message_id']:
        context.bot.delete_message(chat_id, message)

    del context.user_data['message_id']

    return ConversationHandler.END


@send_typing_action
def note_dont_know(update, context):
    context.user_data['message_id'].append(update.effective_message.message_id)
    reply_text = update.message.reply_text(
        'Не понимаю.'
    )
    context.user_data['message_id'].append(reply_text.message_id)

import logging
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

from db import db, get_or_create_chat, get_or_create_user
from settings import API_KEY, PROXY
from utils import get_keyboard

from notes import (note_cancel, note_caption, note_dont_know,
                   note_menu, note_start, note_text, note_clear,
                   )

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update, context):
    user = get_or_create_user(db, update.effective_user)
    chat = get_or_create_chat(db, update.effective_chat)
    update.message.reply_text(
        'Hello_{}!\n This chat is {}'.format(
            user['first_name'],
            chat['chat_id']
        ),
        reply_markup=get_keyboard()
    )


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    ''' Start bot '''
    updater = Updater(API_KEY, request_kwargs=PROXY, use_context=True)

    # Dispatcher to register handler
    dp = updater.dispatcher

    create_note_handler = ConversationHandler(
        entry_points=[
            CommandHandler('note', note_start),
            MessageHandler(Filters.regex('^Create note$'), note_start)
        ],

        states={
            'NOTE_CAPTION': [MessageHandler(Filters.text, note_caption)],
            'NOTE_TEXT': [MessageHandler(Filters.text, note_text)],
            'NOTE_CLEAR_CONVERSATION': [
                MessageHandler(Filters.regex('^Оставить$'), note_cancel),
                MessageHandler(Filters.regex('^Очистить$'), note_clear)
            ]
        },

        fallbacks=[
            MessageHandler(
                Filters.text | Filters.video | Filters.audio | Filters.document | Filters.photo, note_dont_know
            ),
            CommandHandler('cancel', note_cancel)]
    )

    # Handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(create_note_handler)
    dp.add_handler(MessageHandler(Filters.regex('^Notes$'), note_menu))

    # log errors
    dp.add_error_handler(error)

    # Start the bot
    updater.start_polling()
    updater.idle


if __name__ == "__main__":
    main()

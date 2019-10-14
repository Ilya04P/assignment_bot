import logging
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

from db import db, create_chat, create_user
from settings import API_KEY, PROXY
from utils import get_keyboard

from notes import note_body, note_caption, note_start

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update, context):
    user = create_user(db, update.effective_user)
    chat = create_chat(db, update.effective_chat)
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

    # Handlers
    dp.add_handler(CommandHandler('start', start))

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^Заметка$'), note_start)],

        states={
            'NOTE_CAPTION': [MessageHandler(Filters.text, note_caption)],

            'NOTE_BODY': [MessageHandler(Filters.text, note_body)]
        },

        fallbacks=[]
    )

    dp.add_handler(conv_handler)

    # log errors
    dp.add_error_handler(error)

    # Start the bot
    updater.start_polling()
    updater.idle


if __name__ == "__main__":
    main()

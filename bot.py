import logging
from telegram.ext import Updater, CommandHandler

from db import db, create_chat, create_user
from settings import API_KEY, PROXY
from utils import get_keyboard

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

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))

    # log errors
    dp.add_error_handler(error)

    # Start the bot
    updater.start_polling()
    updater.idle


if __name__ == "__main__":
    main()

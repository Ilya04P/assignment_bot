from telegram import ReplyKeyboardRemove


# Start note converstation
def note_start(update, context):
    update.message.reply_text(
        "Добавь заголовок заметки.",
        reply_markup=ReplyKeyboardRemove()
    )

    return 'NOTE_CAPTION'


def note_caption(update, context):
    pass


def note_body(update, context):
    pass

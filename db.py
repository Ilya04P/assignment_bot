from datetime import datetime

from pymongo import MongoClient
import ssl

from settings import MONGO_DB, MONGO_LINK

# Create data base
db = MongoClient(MONGO_LINK, ssl_cert_reqs=ssl.CERT_NONE)[MONGO_DB]


# Create User if not exists
def get_or_create_user(db, effective_user):
    user = db.users.find_one({'user_id': effective_user.id})
    if not user:
        user = {
            'user_id': effective_user.id,
            'first_name': effective_user.first_name,
            'last_name': effective_user.last_name,
            'username': effective_user.username,
            'language_code': effective_user.language_code
        }
        db.users.insert_one(user)
    return user


# Create Chat if not exists
def get_or_create_chat(db, effective_chat):
    chat = db.chats.find_one({'chat_id': effective_chat.id})
    if not chat:
        chat = {
            'chat_id': effective_chat.id,
            'type': effective_chat.type,
            'notes': 0
        }
        db.chats.insert_one(chat)
    return chat


# Create and return chat
def create_note(db, chat, caption, text):
    notes_count = chat['notes']
    time_now = int(datetime.now().timestamp())
    note = {
        'note_id': 'N{}'.format(notes_count + 1),
        'chat_id': chat['_id'],
        'caption': caption,
        'text': text,
        'd_create': time_now,
        'd_modify': time_now
    }
    db.notes.insert_one(note)
    db.chats.update_one(
        {'_id': chat['_id']},
        {'$set': {'notes': notes_count + 1}}
    )

    return note

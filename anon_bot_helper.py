import db
from db import *

def saveUser(message):
    if not db.session.query(User).get(message.chat.id):
        user_from = db.User(id=message.chat.id,
                            first_name=message.from_user.first_name,
                            last_name=message.from_user.last_name,
                            username=message.from_user.username,
                            id_rate=1
                            )
        db.session.add(user_from)
        db.session.commit()


def saveMessageText(message, user_from, user_to):
    msg = db.Message(id_from=user_from,
                     id_to=user_to,
                     text=message.text,
                     media=None,
                     is_delivered=1
                     )
    db.session.add(msg)
    db.session.commit()


def saveMessageSticker(message, user_from, user_to):
    msg = db.Message(id_from=user_from,
                     id_to=user_to,
                     text='sticker',
                     media=message.sticker.file_id,
                     is_delivered=1
                     )
    db.session.add(msg)
    db.session.commit()


def saveMessagePhoto(message, user_from, user_to):
    if not message.caption:
        message.caption = ''

    msg = db.Message(id_from=user_from,
                     id_to=user_to,
                     text=message.caption,
                     media=message.photo[-1].file_id,
                     is_delivered=1
                     )
    db.session.add(msg)
    db.session.commit()


def saveMessageVideo(message, user_from, user_to):
    if not message.caption:
        message.caption = ''

    msg = db.Message(id_from=user_from,
                     id_to=user_to,
                     text='video',
                     media=message.video.file_id,
                     is_delivered=1
                     )
    db.session.add(msg)
    db.session.commit()


def saveMessageVoice(message, user_from, user_to):
    msg = db.Message(id_from=user_from,
                     id_to=user_to,
                     text='voice',
                     media=message.voice.file_id,
                     is_delivered=1
                     )
    db.session.add(msg)
    db.session.commit()


def saveMessageVideoNote(message, user_from, user_to):
    msg = db.Message(id_from=user_from,
                     id_to=user_to,
                     text='video_note',
                     media=message.video_note.file_id,
                     is_delivered=1
                     )
    db.session.add(msg)
    db.session.commit()
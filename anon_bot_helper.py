import db
from db import *


def saveUser(message):
    if not db.session.query(User).get(message.chat.id):
        user_from = db.User(id=message.chat.id,
                            first_name=message.from_user.first_name,
                            last_name=message.from_user.last_name,
                            username=message.from_user.username,
                            id_rate=1,
                            balance=0
                            )
        db.session.add(user_from)
        db.session.commit()


def saveMessageText(message, user_from, user_to):
    msg = db.Message(id_from=user_from,
                     id_to=user_to,
                     content_type='text',
                     text=message.text,
                     media=None,
                     is_delivered=1
                     )
    db.session.add(msg)
    db.session.commit()


def saveMessageSticker(message, user_from, user_to):
    msg = db.Message(id_from=user_from,
                     id_to=user_to,
                     content_type='sticker',
                     text=None,
                     media=message.sticker.file_id,
                     is_delivered=1
                     )
    db.session.add(msg)
    db.session.commit()


def saveMessagePhoto(message, user_from, user_to):
    msg = db.Message(id_from=user_from,
                     id_to=user_to,
                     content_type='photo',
                     text=message.caption,
                     media=message.photo[-1].file_id,
                     is_delivered=1
                     )
    db.session.add(msg)
    db.session.commit()


def saveMessageVideo(message, user_from, user_to):
    msg = db.Message(id_from=user_from,
                     id_to=user_to,
                     content_type='video',
                     text=message.caption,
                     media=message.video.file_id,
                     is_delivered=1
                     )
    db.session.add(msg)
    db.session.commit()


def saveMessageVoice(message, user_from, user_to):
    msg = db.Message(id_from=user_from,
                     id_to=user_to,
                     content_type='voice',
                     text=None,
                     media=message.voice.file_id,
                     is_delivered=1
                     )
    db.session.add(msg)
    db.session.commit()


def saveMessageVideoNote(message, user_from, user_to):
    msg = db.Message(id_from=user_from,
                     id_to=user_to,
                     content_type='video_note',
                     text=None,
                     media=message.video_note.file_id,
                     is_delivered=1
                     )
    db.session.add(msg)
    db.session.commit()


def getLatestUserToId(id_from):
    message = db.session.query(Message).order_by(Message.date.desc()).filter_by(id_from=id_from).first()
    return message.id_to


def getBalanceByUserId(id):
    return db.session.query(User).get(id).balance


def countIncomingMessagesByUserId(id) -> int:
    return db.session.query(Message).filter_by(id_to=id).count()


def countOutcomingMessagesByUserId(id) -> int:
    return db.session.query(Message).filter_by(id_from=id).count()

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


def getRates():
    return db.session.query(Rate).filter(Rate.price.is_not(None))


def getRateById(id):
    return db.session.query(Rate).get(id)

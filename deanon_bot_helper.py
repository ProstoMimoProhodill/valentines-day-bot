import db
from db import *


def saveUser(message):
    if not db.session.query(User).get(message.chat.id):
        user_from = db.User(id=message.chat.id,
                            first_name=message.from_user.first_name,
                            last_name=message.from_user.last_name,
                            username=message.from_user.username,
                            id_rate=1,
                            balance=0)
        db.session.add(user_from)
        db.session.commit()


def getUserById(id):
    return db.session.query(User).get(id)


def getRates():
    return db.session.query(Rate).filter(Rate.price.is_not(None))


def getRateById(id):
    return db.session.query(Rate).get(id)


def getFriendCountByUserId(id):
    return db.session.query(User).get(id).friend_count


def setFriendCountByUserId(id, val):
    user = db.session.query(User).get(id)
    user.friend_count = val
    db.session.commit()


def setRateByUserId(id, val):
    user = db.session.query(User).get(id)
    user.id_rate = val
    db.session.commit()


def getBalanceByUserId(id):
    return db.session.query(User).get(id).balance


def setBalanceByUserId(id, val):
    user = db.session.query(User).get(id)
    user.balance = val
    db.session.commit()


def savePayment(id_user, id_rate, price, concurrency):
    payment = Payment(id_user=id_user,
                      id_rate=id_rate,
                      price=price,
                      concurrency=concurrency)
    db.session.add(payment)
    db.session.commit()


def saveFriend(id_user, id_friend):
    friend = Friend(id_user=id_user,
                    id_friend=id_friend)
    db.session.add(friend)
    db.session.commit()


def getFriend(id_user, id_friend):
    return db.session.query(Friend).filter_by(id_user=id_user, id_friend=id_friend).all()

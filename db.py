import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine('sqlite:///sqlite3.db', connect_args={'check_same_thread': False})

Base = declarative_base()

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_from = Column(Integer, ForeignKey('users.id'), nullable=False)
    id_to = Column(Integer, ForeignKey('users.id'), nullable=False)
    content_type = Column(String, nullable=False)
    text = Column(Text, nullable=True)
    media = Column(String, nullable=True)
    is_delivered = Column(Boolean, nullable=False)
    date = Column(DateTime, default=datetime.now())

    user_from = relationship('User', foreign_keys=[id_from], uselist=False)
    user_to = relationship('User', foreign_keys=[id_to], uselist=False)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    username = Column(String, nullable=False)
    id_rate = Column(Integer, ForeignKey('rates.id'), nullable=False)
    # balance - сколько можешь задеанонить посланий
    balance = Column(Integer, default=0, nullable=False)
    friend_count = Column(Integer, default=0, nullable=False)

    rate = relationship('Rate', foreign_keys="User.id_rate", uselist=False)


class Friend(Base):
    __tablename__ = 'friends'
    id_user = Column(Integer, primary_key=True, autoincrement=False)
    id_friend = Column(Integer, primary_key=True, autoincrement=False)


class Rate(Base):
    __tablename__ = 'rates'
    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(Integer, nullable=True)
    concurrency = Column(String, nullable=True)
    full_balance = Column(Integer, nullable=True)
    description = Column(String, nullable=False)


class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    id_rate = Column(Integer, ForeignKey('rates.id'), nullable=False)
    price = Column(Integer, nullable=False)
    concurrency = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.now())

    user = relationship('User', foreign_keys="Payment.id_user", uselist=False)
    rate = relationship('Rate', foreign_keys="Payment.id_rate", uselist=False)


def generateRates(s):
    rates = [
        Rate(price=None, concurrency=None, full_balance=None, description='Тариф не выбран'),
        Rate(price=79, concurrency='RUB', full_balance=5, description='Деанон 5ти посланий'),
        Rate(price=150, concurrency='RUB', full_balance=10000, description='Безлимитный деанон'),
        Rate(price=3, concurrency='FRIEND', full_balance=3, description='Деанон 3х посланий'),
        Rate(price=5, concurrency='FRIEND', full_balance=5, description='Деанон 5х посланий'),
        Rate(price=10, concurrency='FRIEND', full_balance=10000, description='Безлимитный деанон')
    ]
    s.add_all(rates)
    s.commit()


def generateUsers(s):
    users = [
        User(id=5641561, first_name='Andrew', last_name='Gilenko', username='@andrew', id_rate=4, balance=0),
        User(id=1561515, first_name='Daria', last_name='Papulova', username='@daria', id_rate=1, balance=0)
    ]
    s.add_all(users)
    s.commit()


def generateMessages(s):
    messages = [
        Message(id_from=5641561, id_to=1561515, content_type='text', text='Андрей Даше', media=None, is_delivered=1),
        Message(id_from=1561515, id_to=5641561, content_type='text', text='Даша Андрею', media=None, is_delivered=1)
    ]
    s.add_all(messages)
    s.commit()


def generatePayments(s):
    payments = [
        Payment(id_user=5641561, id_rate=2, price=250, concurrency='RUB')
    ]
    s.add_all(payments)
    s.commit()


def showRates(s):
    for rate in s.query(Rate).all():
        print(f'{rate.id} {rate.price} {rate.concurrency} {rate.description}')


def showUsers(s):
    for user in s.query(User).all():
        print(f'{user.id} {user.first_name} {user.last_name} {user.username} {user.id_rate}')


def showMessages(s):
    for msg in s.query(Message).all():
        print(f'{msg.id} {msg.id_from} {msg.id_to} {msg.text} {msg.media} {msg.is_delivered} {msg.date}')


def showPayments(s):
    for payment in s.query(Payment).all():
        print(f'{payment.id} {payment.id_user} {payment.price} {payment.date}')


def clearDataBase():
    Base.metadata.drop_all(engine)


def createTables():
    Base.metadata.create_all(engine)

# clearDataBase()
# createTables()
#
# generateRates(session)
# showRates(session)

# generateUsers(session)
# showUsers(session)

# generateMessages(session)
# showMessages(session)

# generatePayments(session)
# showPayments(session)

# for msg in session.query(Message).filter_by(id_to=437499696).count():
#     print(f'{msg.id} {msg.id_from} {msg.id_to} {msg.text} {msg.media} {msg.is_delivered} {msg.date}')

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
    text = Column(Text, nullable=False)
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
    # balance = Column(Integer, nullable=True)

    rate = relationship('Rate', foreign_keys="User.id_rate", uselist=False)

class Rate(Base):
    __tablename__ = 'rates'
    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(Integer, nullable=True)
    description = Column(Text, nullable=False)

class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    price = Column(Integer, nullable=False)
    date = Column(DateTime, default=datetime.now())

    user = relationship('User', foreign_keys="Payment.id_user", uselist=False)

def generateRates(s):
    rates = [
            Rate(price=None, description='Бесплатно'),
            Rate(price=50, description='1й тариф'),
            Rate(price=150, description='2й тариф'),
            Rate(price=250, description='3й тариф')
        ]
    s.add_all(rates)
    s.commit()

def generateUsers(s):
    users = [
        User(id=5641561, first_name='Andrew', last_name='Gilenko', username='@andrew', id_rate=4),
        User(id=1561515, first_name='Daria', last_name='Papulova', username='@daria', id_rate=1)
    ]
    s.add_all(users)
    s.commit()

def generateMessages(s):
    messages = [
        Message(id_from=5641561, id_to=1561515, text='Андрей Даше', media=None, is_delivered=1),
        Message(id_from=1561515, id_to=5641561, text='Даша Андрею', media=None, is_delivered=0)
    ]
    s.add_all(messages)
    s.commit()

def generatePayments(s):
    payments = [
        Payment(id_user=5641561, price=250)
    ]
    s.add_all(payments)
    s.commit()

def showRates(s):
    for rate in s.query(Rate).all():
        print(f'{rate.id} {rate.price} {rate.description}')

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

# generateRates(session)
# showRates(session)

# generateUsers(session)
# showUsers(session)

# generateMessages(session)
# showMessages(session)

# generatePayments(session)
# showPayments(session)



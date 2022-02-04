import db
import sys
import telebot
from db import *
from telebot import types
from telebot.storage import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State


def main():
    if 'deanon_your_valentines_bot_token' in os.environ:
        token = os.environ['deanon_your_valentines_bot_token']
    else:
        print('token not found')
        sys.exit(0)

    bot_url = 'deanon_your_valentines_bot'
    state_storage = StateMemoryStorage()
    bot = telebot.TeleBot(token, state_storage=state_storage)

    class States(StatesGroup):
        user = State()

    @bot.message_handler(commands=['start'])
    def start(message):
        provider_token = '381764678:TEST:33280'
        bot.send_invoice(message.chat.id,
                         title='Деанон',
                         description='Описание',
                         invoice_payload='false',
                         provider_token=provider_token,
                         currency='RUB',
                         start_parameter='test',
                         prices=[
                             types.LabeledPrice(label='Руб', amount=100 * 100)
                         ]
                         )

    @bot.pre_checkout_query_handler(func=lambda call: True)
    def payment(message):
        bot.answer_pre_checkout_query(message.id, ok=True)
        print(message)

    bot.infinity_polling()

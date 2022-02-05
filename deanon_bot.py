import sys
from deanon_bot_helper import *
from deanon_bot_templates import *
from telebot import types
from telebot import telebot
from telebot.storage import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State

import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y/%m/%d %H:%M:%S',
                    handlers=[
                        logging.FileHandler('deanon_output.log'),
                        logging.StreamHandler()
                    ])


class States(StatesGroup):
    user = State()


def main():
    if 'deanon_your_valentines_bot_token' in os.environ:
        token = os.environ['deanon_your_valentines_bot_token']
    else:
        logging.error('token not found')
        sys.exit(0)

    bot = telebot.TeleBot(token, state_storage=StateMemoryStorage())
    bot.set_my_commands([
        telebot.types.BotCommand('/stats', 'My stats📈')
    ])

    @bot.message_handler(commands=['start'])
    def start(message):
        saveUser(message)
        rates = getRates()
        msg, markup = templateMessageShowRates(rates, types.InlineKeyboardMarkup())
        bot.send_message(message.chat.id,
                         msg,
                         parse_mode='Markdown',
                         reply_markup=markup)

    @bot.message_handler(commands=['start'])
    def activateReferralLink(message):
        # TODO
        pass

    @bot.callback_query_handler(func=lambda call: True)
    def selectedRate(call):
        bot.answer_callback_query(call.id)

        id_rate = call.data
        rate = getRateById(id_rate)

        if rate.concurrency == 'RUB':
            payment(call.message.chat.id, 'Оплата', rate.description, rate.price)
        elif rate.concurrency == 'FRIEND':
            bot.send_message(call.message.chat.id, templateMessageReferralLink(call.message))

    def payment(chat_id, title, description, price):
        provider_token = '381764678:TEST:33280'
        bot.send_invoice(chat_id,
                         title=title,
                         description=description,
                         invoice_payload='false',
                         provider_token=provider_token,
                         currency='RUB',
                         start_parameter='test',
                         prices=[
                             types.LabeledPrice(label='Руб', amount=price * 100)
                         ]
                         )

    @bot.pre_checkout_query_handler(func=lambda call: True)
    def confirmPayment(message):
        bot.answer_pre_checkout_query(message.id, ok=True)

    @bot.message_handler(content_types=['successful_payment'])
    def successfulPayment(message):
        bot.send_message(message.chat.id, templateMessageSuccessfulPayment())

    bot.infinity_polling()


if __name__ == '__main__':
    main()
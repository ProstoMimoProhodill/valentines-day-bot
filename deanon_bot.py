import sys
import filecmp
from deanon_bot_helper import *
from deanon_bot_templates import *
from config import anon_bot_url
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
    id_user = State()
    id_rate = State()
    price = State()
    concurrency = State()


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

    @bot.message_handler(commands=['start'],
                         func=lambda msg: len(msg.text.split()) == 1)
    def start(message):
        saveUser(message)
        showRates(message)

    @bot.message_handler(commands=['start'],
                         func=lambda msg: msg.text.split()[1].split('-')[1] == 'referral')
    def activateReferralLink(message):
        saveUser(message)
        id_user = int(message.from_user.id)
        id_user_from = int(message.text.split()[1].split('-')[0])
        if id_user != id_user_from:
            friend = getFriend(id_user_from, id_user)
            if friend:
                return
            bot.send_message(id_user, templateMessageActivateReferralLink())
            bot.send_message(id_user_from, templateMessageActivateReferralLinkUserFrom())
            friend_count = int(getFriendCountByUserId(id_user_from))
            setFriendCountByUserId(id_user_from, friend_count + 1)
            saveFriend(id_user_from, id_user)

    @bot.callback_query_handler(func=lambda call: True)
    def selectedRate(call):
        bot.answer_callback_query(call.id)

        id_rate = int(call.data)
        rate = getRateById(id_rate)

        if rate.concurrency == 'RUB':
            payment(call.message.chat.id, 'Оплата', rate.description, rate.price)
        elif rate.concurrency == 'FRIEND':
            friend_count = int(getFriendCountByUserId(call.message.chat.id))
            price = int(rate.price)
            if friend_count < price:
                bot.send_message(call.message.chat.id, templateMessageReferralLink(call.message))
            else:
                setRateByUserId(call.message.chat.id, id_rate)
                user_balance = getBalanceByUserId(call.message.chat.id)
                setBalanceByUserId(call.message.chat.id, user_balance + rate.full_balance)
                setFriendCountByUserId(call.message.chat.id, friend_count - price)
                savePayment(call.message.chat.id, id_rate, rate.price, rate.concurrency)
                bot.send_message(call.message.chat.id, templateMessageSuccessfulPayment())

        bot.set_state(call.message.chat.id, States.id_user, call.message.chat.id)
        with bot.retrieve_data(call.message.chat.id, call.message.chat.id) as data:
            data['id_user'] = int(call.message.chat.id)
            data['id_rate'] = int(id_rate)
            data['price'] = rate.price
            data['concurrency'] = rate.concurrency

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
                         ])

    @bot.pre_checkout_query_handler(func=lambda call: True)
    def confirmPayment(message):
        bot.answer_pre_checkout_query(message.id, ok=True)

    @bot.message_handler(content_types=['successful_payment'])
    def successfulPayment(message):
        with bot.retrieve_data(message.chat.id, message.chat.id) as data:
            setRateByUserId(data['id_user'], data['id_rate'])
            user_balance = getBalanceByUserId(message.chat.id)
            full_balance = getRateById(data['id_rate']).full_balance
            setBalanceByUserId(data['id_user'], user_balance + full_balance)
            savePayment(data['id_user'], data['id_rate'], data['price'], data['concurrency'])
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(message.chat.id, templateMessageSuccessfulPayment())

    @bot.message_handler(content_types=['text'],
                         func=lambda msg: msg.forward_from.username == anon_bot_url)
    def deanonTextMessage(message):
        user_balance = getBalanceByUserId(message.chat.id)
        if user_balance <= 0:
            showRates(message)
            return

        id_user_from = getUserFrom(message.chat.id, message.content_type, message.text)
        user = getUserById(id_user_from)

        setBalanceByUserId(message.chat.id, user_balance - 1)
        bot.reply_to(message, templateMessageDeanon(user_balance - 1, user.username), parse_mode='Markdown')

    @bot.message_handler(content_types=['photo'],
                         func=lambda msg: msg.forward_from.username == anon_bot_url)
    def deanonPhotoMessage(message):
        user_balance = getBalanceByUserId(message.chat.id)
        if user_balance <= 0:
            showRates(message)
            return

        # file from reply
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        file = bot.download_file(file_info.file_path)

        # get messages
        messages = getMessages(message.chat.id, message.content_type)

        # compare files and find our file
        id_user_from = None
        for msg in messages:
            if not msg.media:
                continue
            with open(f'media/{msg.media}.jpg', 'rb') as file_db:
                file_db_byte_array = file_db.read()
                if file_db_byte_array == file:
                    id_user_from = msg.id_from
                    break

        # find user and reply userinfo
        if not id_user_from:
            return
        user = getUserById(id_user_from)
        setBalanceByUserId(message.chat.id, user_balance - 1)
        bot.reply_to(message, templateMessageDeanon(user_balance - 1, user.username), parse_mode='Markdown')

    @bot.message_handler(content_types=['video'],
                         func=lambda msg: msg.forward_from.username == anon_bot_url)
    def deanonVideoMessage(message):
        user_balance = getBalanceByUserId(message.chat.id)
        if user_balance <= 0:
            showRates(message)
            return

        # file from reply
        file_id = message.video.file_id
        file_info = bot.get_file(file_id)
        file = bot.download_file(file_info.file_path)

        # get messages
        messages = getMessages(message.chat.id, message.content_type)

        # compare files and find our file
        id_user_from = None
        for msg in messages:
            if not msg.media:
                continue
            with open(f'media/{msg.media}.mp4', 'rb') as file_db:
                file_db_byte_array = file_db.read()
                if file_db_byte_array == file:
                    id_user_from = msg.id_from
                    break

        # find user and reply userinfo
        if not id_user_from:
            return
        user = getUserById(id_user_from)
        setBalanceByUserId(message.chat.id, user_balance - 1)
        bot.reply_to(message, templateMessageDeanon(user_balance - 1, user.username), parse_mode='Markdown')

    @bot.message_handler(content_types=['video_note'],
                         func=lambda msg: msg.forward_from.username == anon_bot_url)
    def deanonVideoNoteMessage(message):
        user_balance = getBalanceByUserId(message.chat.id)
        if user_balance <= 0:
            showRates(message)
            return

        # file from reply
        file_id = message.video_note.file_id
        file_info = bot.get_file(file_id)
        file = bot.download_file(file_info.file_path)

        # get messages
        messages = getMessages(message.chat.id, message.content_type)

        # compare files and find our file
        id_user_from = None
        for msg in messages:
            if not msg.media:
                continue
            with open(f'media/{msg.media}.mp4', 'rb') as file_db:
                file_db_byte_array = file_db.read()
                if file_db_byte_array == file:
                    id_user_from = msg.id_from
                    break

        # find user and reply userinfo
        if not id_user_from:
            return
        user = getUserById(id_user_from)
        setBalanceByUserId(message.chat.id, user_balance - 1)
        bot.reply_to(message, templateMessageDeanon(user_balance - 1, user.username), parse_mode='Markdown')

    @bot.message_handler(content_types=['voice'],
                         func=lambda msg: msg.forward_from.username == anon_bot_url)
    def deanonVoiceMessage(message):
        user_balance = getBalanceByUserId(message.chat.id)
        if user_balance <= 0:
            showRates(message)
            return

        # file from reply
        file_id = message.voice.file_id
        file_info = bot.get_file(file_id)
        file = bot.download_file(file_info.file_path)

        # get messages
        messages = getMessages(message.chat.id, message.content_type)

        # compare files and find our file
        id_user_from = None
        for msg in messages:
            if not msg.media:
                continue
            with open(f'media/{msg.media}.mp3', 'rb') as file_db:
                file_db_byte_array = file_db.read()
                if file_db_byte_array == file:
                    id_user_from = msg.id_from
                    break

        # find user and reply userinfo
        if not id_user_from:
            return
        user = getUserById(id_user_from)
        setBalanceByUserId(message.chat.id, user_balance - 1)
        bot.reply_to(message, templateMessageDeanon(user_balance - 1, user.username), parse_mode='Markdown')

    @bot.message_handler(content_types=['sticker'],
                         func=lambda msg: msg.forward_from.username == anon_bot_url)
    def deanonStickerMessage(message):
        user_balance = getBalanceByUserId(message.chat.id)
        if user_balance <= 0:
            showRates(message)
            return

        # file from reply
        file_id = message.sticker.thumb.file_id
        file_info = bot.get_file(file_id)
        file = bot.download_file(file_info.file_path)

        # get messages
        messages = getMessages(message.chat.id, message.content_type)

        # compare files and find our file
        id_user_from = None
        for msg in messages:
            if not msg.media:
                continue
            with open(f'media/{msg.media}.jpg', 'rb') as file_db:
                file_db_byte_array = file_db.read()
                if file_db_byte_array == file:
                    id_user_from = msg.id_from
                    break

        # find user and reply userinfo
        if not id_user_from:
            return
        user = getUserById(id_user_from)
        setBalanceByUserId(message.chat.id, user_balance - 1)
        bot.reply_to(message, templateMessageDeanon(user_balance - 1, user.username), parse_mode='Markdown')

    def showRates(message):
        rates = getRates()
        user_balance = getBalanceByUserId(message.chat.id)
        msg, markup = templateMessageShowRates(user_balance, rates, types.InlineKeyboardMarkup())
        bot.send_message(message.chat.id,
                         msg,
                         parse_mode='Markdown',
                         reply_markup=markup)

    bot.infinity_polling()


if __name__ == '__main__':
    main()

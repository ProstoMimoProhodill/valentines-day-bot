from telebot import types
from config import deanon_bot_url


def templateMessageSuccessfulPayment() -> str:
    return f'Оплата прошла успешно!\n'


def templateMessageReferralLink(message) -> str:
    return f'Твоя реферальная ссылка:\n' \
           f'\n' \
           f't.me/{deanon_bot_url}?start={message.chat.id}-referral\n' \
           f'\n' \
           f'Отправь её своим друзьям и у тебя пополнится баланс❤\n' \
           f'Отслеживать свой баланс можно в Menu->My stats📈\n'


def templateMessageActivateReferralLink():
    return f'Ссылка активирована!\n'


def templateMessageActivateReferralLinkUserFrom():
    return f'Кто-то активировал твою ссылку!\n'


def templateMessageShowRates(rates, markup):
    message = '_Доступные тарифы_: \n\n'
    for rate in rates:
        msg = ''
        callback_data = rate.id
        if rate.concurrency == 'RUB':
            msg += f'{rate.price} РУБ🇷🇺 - {rate.description}\n'
        elif rate.concurrency == 'FRIEND':
            if rate.price == 5 or rate.price == 10:
                msg += f'{rate.price} друзей🖐 - {rate.description}\n'
            else:
                msg += f'{rate.price} друга🖐 - {rate.description}\n'
        button = types.InlineKeyboardButton(msg, callback_data=callback_data)
        markup.row(button)
    return message, markup

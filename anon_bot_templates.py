from config import bot_url

def templateMessageGetStats(data) -> str:
    return f'👉Полученные: {data["incoming"]}\n' \
           f'👈Отправленные: {data["outcoming"]}\n' \
           f'Баланс: ...\n'


def templateMessageReferralLink(message) -> str:
    return f'Твоя реферальная ссылка:\n' \
           f'\n' \
           f't.me/{bot_url}?referral={message.chat.id}\n'


def templateMessageDeanonLink() -> str:
    return f'[Смотреть от кого приходят валентинки можно через бота](http://t.me/deanon_your_valentines_bot)'


def templateMessageReferralLink(message, ) -> str:
    return f'Твоя реферальная ссылка:\n' \
           f'\n' \
           f't.me/{bot_url}?referral={message.chat.id}\n'

def templateMessageFrom(message) -> str:
    return f'Готово, твое сообщение отправлено!\n' \
           f'\n' \
           f'Вот твоя ссылка для приема анонимных валентинок:\n' \
           f'\n' \
           f't.me/{bot_url}?start={message.chat.id}\n' \
           f'\n' \
           f'Размести её у себя в инстаграме и расскажи о ней в сторис и твои знакомые начнут присылать ' \
           f'тебе валентинки '


def templateMessageTo() -> str:
    return f'[У вас новое признание:](http://t.me/deanon_your_valentines_bot)\n '


def templateMessageToWithText(message) -> str:
    return f'[У вас новое признание:](http://t.me/deanon_your_valentines_bot)\n\n*{message.text}* '


def templateMessageToWithCaption(message) -> str:
    return f'[У вас новое признание:](http://t.me/deanon_your_valentines_bot)\n\n*{message.caption}* '


def templateMessageStartByLink() -> str:
    return f"Здесь ты можешь анонимно рассказать, что думаешь о человеке, который опубликовал эту ссылку\n" \
           f"\n" \
           f"Напиши это сюда в одном сообщении и через несколько мгновений он его получит, но не будет знать от " \
           f"кого оно "


def templateMessageStart(message) -> str:
    return f"Вот твоя ссылка для приема анонимных валентинок:\n" \
           f"\n" \
           f"t.me/{bot_url}?start={message.chat.id}\n" \
           f"\n" \
           f"Размести её у себя в инстаграме и расскажи о ней в сторис и твои знакомые начнут присылать тебе " \
           f"валентинки "
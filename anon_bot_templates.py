from config import anon_bot_url

def templateMessageGetStats(data) -> str:
    return f'Баланс:  {data["balance"]}  ❤\n' \
           f'Отправленные:  {data["outcoming"]}  👈\n' \
           f'Полученные:  {data["incoming"]}  👉\n'


def templateMessageReferralLink(message) -> str:
    return f'Твоя реферальная ссылка:\n' \
           f'\n' \
           f't.me/{anon_bot_url}?referral={message.chat.id}\n'


def templateMessageDeanonLink() -> str:
    return f'[Смотреть от кого приходят валентинки можно через бота](http://t.me/deanon_your_valentines_bot)'


def templateMessageReferralLink(message) -> str:
    return f'Твоя реферальная ссылка:\n' \
           f'\n' \
           f't.me/{anon_bot_url}?referral={message.chat.id}\n'

def templateMessageFrom(message) -> str:
    return f'Готово, твое сообщение отправлено!\n' \
           f'\n' \
           f'Вот твоя ссылка для приема анонимных валентинок:\n' \
           f'\n' \
           f't.me/{anon_bot_url}?start={message.chat.id}\n' \
           f'\n' \
           f'Размести её у себя в инстаграме и расскажи о ней в сторис и твои знакомые начнут присылать ' \
           f'тебе валентинки '


def templateMessageTo() -> str:
    return f'[У вас новое признание:](http://t.me/deanon_your_valentines_bot)'


def templateMessageToWithText(message) -> str:
    return f'*{message.text}* '


def templateMessageToWithCaption(message) -> str:
    return f'*{message.caption}* '


def templateMessageStartByLink() -> str:
    return f"Здесь ты можешь анонимно рассказать, что думаешь о человеке, который опубликовал эту ссылку\n" \
           f"\n" \
           f"Напиши это сюда в одном сообщении и через несколько мгновений он его получит, но не будет знать от " \
           f"кого оно\n" \
           f"\n" \
           f"Если хочешь отправить еще сообщение, то перейди в Меню->Новое сообщение👉\n"


def templateMessageNewMessage() -> str:
    return f"Здесь ты можешь анонимно рассказать, что думаешь о человеке, который опубликовал эту ссылку\n"


def templateMessageStart(message) -> str:
    return f"Вот твоя ссылка для приема анонимных валентинок:\n" \
           f"\n" \
           f"t.me/{anon_bot_url}?start={message.chat.id}\n" \
           f"\n" \
           f"Размести её у себя в инстаграме и расскажи о ней в сторис и твои знакомые начнут присылать тебе " \
           f"валентинки "

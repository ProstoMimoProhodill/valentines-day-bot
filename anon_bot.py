import db
import sys
import telebot
from db import *
from telebot.storage import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State


def main():
    if 'get_your_valentines_bot_token' in os.environ:
        token = os.environ['get_your_valentines_bot_token']
    else:
        print('token not found')
        sys.exit(0)

    bot_url = 'get_your_valentines_bot'
    state_storage = StateMemoryStorage()
    bot = telebot.TeleBot(token, state_storage=state_storage)

    class States(StatesGroup):
        user_to = State()
        user_from = State()
        is_ready_to_send_message = State()

    @bot.message_handler(commands=['start'])
    def start(message):
        chat_id = message.chat.id

        if not db.session.query(User).get(chat_id):
            user_from = db.User(id=chat_id,
                                first_name=message.from_user.first_name,
                                last_name=message.from_user.last_name,
                                username=message.from_user.username,
                                id_rate=1
                                )
            db.session.add(user_from)
            db.session.commit()

        if len(message.text.split()) > 1:
            id_to = message.text.split()[1]
            msg_to = f'Здесь ты можешь анонимно рассказать, что думаешь о человеке, который опубликовал эту ссылку\n' \
                     f'\n' \
                     f'Напиши это сюда в одном сообщении и через несколько мгновений он его получит, но не будет знать от ' \
                     f'кого оно '
            bot.send_message(chat_id, msg_to)
            bot.set_state(message.from_user.id, States.is_ready_to_send_message, chat_id)
            with bot.retrieve_data(message.from_user.id, chat_id) as data:
                data['is_ready_to_send_message'] = True
                data['user_from'] = int(chat_id)
                data['user_to'] = int(id_to)
        else:
            msg = f'Вот твоя ссылка для приема анонимных валентинок:\n' \
                  f'\n' \
                  f't.me/{bot_url}?start={chat_id}\n' \
                  f'\n' \
                  f'Размести её у себя в инстаграме и расскажи о ней в сторис и твои знакомые начнут присылать тебе ' \
                  f'валентинки '
            bot.send_message(chat_id, msg)

    @bot.message_handler(content_types=['text', 'photo', 'sticker', 'voice', 'video_note'])
    @bot.message_handler(state=States.is_ready_to_send_message)
    def comfirm(message):
        user_id = message.from_user.id
        chat_id = message.chat.id

        if not bot.get_state(user_id, chat_id):
            return

        with bot.retrieve_data(user_id, chat_id) as data:
            print(data)

            if message.content_type == 'text':
                msg = db.Message(id_from=data['user_from'],
                                 id_to=data['user_to'],
                                 text=message.text,
                                 media=None,
                                 is_delivered=1
                                 )
                db.session.add(msg)
                db.session.commit()

                msg_from = f"Готово, твое сообщение отправлено!\n" \
                           f"\n" \
                           f"Вот твоя ссылка для приема анонимных валентинок:\n" \
                           f"\n" \
                           f"t.me/{bot_url}?start={chat_id}\n" \
                           f"\n" \
                           f"Размести её у себя в инстаграме и расскажи о ней в сторис и твои знакомые начнут присылать " \
                           f"тебе валентинки "
                bot.send_message(data['user_from'], msg_from)

                msg_to = f'У вас новое признание:\n\n*{message.text}*'
                bot.send_message(data['user_to'], msg_to, parse_mode='Markdown')
            elif message.content_type == 'sticker':
                msg = db.Message(id_from=data['user_from'],
                                 id_to=data['user_to'],
                                 text='sticker',
                                 media=message.sticker.file_id,
                                 is_delivered=1
                                 )
                db.session.add(msg)
                db.session.commit()

                msg_from = f"Готово, твое сообщение отправлено!\n" \
                           f"\n" \
                           f"Вот твоя ссылка для приема анонимных валентинок:\n" \
                           f"\n" \
                           f"t.me/{bot_url}?start={chat_id}\n" \
                           f"\n" \
                           f"Размести её у себя в инстаграме и расскажи о ней в сторис и твои знакомые начнут присылать " \
                           f"тебе валентинки "
                bot.send_message(data['user_from'], msg_from)

                msg_to = f'У вас новое признание:\n'
                bot.send_message(data['user_to'], msg_to)
                bot.send_sticker(data['user_to'], message.sticker.file_id)
            elif message.content_type == 'photo':
                if not message.caption:
                    message.caption = ''

                msg = db.Message(id_from=data['user_from'],
                                 id_to=data['user_to'],
                                 text=message.caption,
                                 media=message.photo[-1].file_id,
                                 is_delivered=1
                                 )
                db.session.add(msg)
                db.session.commit()

                file_id = message.photo[-1].file_id
                file_info = bot.get_file(file_id)
                file = bot.download_file(file_info.file_path)
                with open(f'media/{file_id}.jpg', 'wb') as photo:
                    photo.write(file)

                msg_from = f"Готово, твое сообщение отправлено!\n" \
                           f"\n" \
                           f"Вот твоя ссылка для приема анонимных валентинок:\n" \
                           f"\n" \
                           f"t.me/{bot_url}?start={chat_id}\n" \
                           f"\n" \
                           f"Размести её у себя в инстаграме и расскажи о ней в сторис и твои знакомые начнут присылать " \
                           f"тебе валентинки "
                bot.send_message(data['user_from'], msg_from)

                msg_to = f'У вас новое признание:\n\n*{message.caption}*'
                bot.send_message(data['user_to'], msg_to, parse_mode='Markdown')
                bot.send_photo(data['user_to'], message.photo[-1].file_id)
            elif message.content_type == 'voice':
                msg = db.Message(id_from=data['user_from'],
                                 id_to=data['user_to'],
                                 text='voice',
                                 media=message.voice.file_id,
                                 is_delivered=1
                                 )
                db.session.add(msg)
                db.session.commit()

                file_id = message.voice.file_id
                file_info = bot.get_file(file_id)
                file = bot.download_file(file_info.file_path)
                with open(f'media/{file_id}.mp3', 'wb') as voice:
                    voice.write(file)

                msg_from = f"Готово, твое сообщение отправлено!\n" \
                           f"\n" \
                           f"Вот твоя ссылка для приема анонимных валентинок:\n" \
                           f"\n" \
                           f"t.me/{bot_url}?start={chat_id}\n" \
                           f"\n" \
                           f"Размести её у себя в инстаграме и расскажи о ней в сторис и твои знакомые начнут присылать " \
                           f"тебе валентинки "
                bot.send_message(data['user_from'], msg_from)

                msg_to = f'У вас новое признание:\n'
                bot.send_message(data['user_to'], msg_to)
                bot.send_voice(data['user_to'], message.voice.file_id)
            elif message.content_type == 'video_note':
                msg = db.Message(id_from=data['user_from'],
                                 id_to=data['user_to'],
                                 text='video_note',
                                 media=message.video_note.file_id,
                                 is_delivered=1
                                 )
                db.session.add(msg)
                db.session.commit()

                file_id = message.video_note.file_id
                file_info = bot.get_file(file_id)
                file = bot.download_file(file_info.file_path)
                with open(f'media/{file_id}.mp4', 'wb') as video_note:
                    video_note.write(file)

                msg_from = f"Готово, твое сообщение отправлено!\n" \
                           f"\n" \
                           f"Вот твоя ссылка для приема анонимных валентинок:\n" \
                           f"\n" \
                           f"t.me/{bot_url}?start={chat_id}\n" \
                           f"\n" \
                           f"Размести её у себя в инстаграме и расскажи о ней в сторис и твои знакомые начнут присылать " \
                           f"тебе валентинки "
                bot.send_message(data['user_from'], msg_from)

                msg_to = f'У вас новое признание:\n'
                bot.send_message(data['user_to'], msg_to)
                bot.send_video_note(data['user_to'], message.video_note.file_id)

        bot.delete_state(user_id, chat_id)

    bot.infinity_polling()

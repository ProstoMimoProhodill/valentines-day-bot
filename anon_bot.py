import sys
import telebot
from anon_bot_helper import *
from anon_bot_templates import *
from telebot.storage import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State


def main():
    if 'get_your_valentines_bot_token' in os.environ:
        token = os.environ['get_your_valentines_bot_token']
    else:
        print('token not found')
        sys.exit(0)

    bot = telebot.TeleBot(token, state_storage=StateMemoryStorage())

    class States(StatesGroup):
        user_to = State()
        user_from = State()
        is_ready_to_send_message = State()

    @bot.message_handler(commands=['start'],
                         func=lambda msg: len(msg.text.split()) == 1)
    def start(message):
        saveUser(message)
        bot.send_message(message.chat.id, templateMessageStart(message))

    @bot.message_handler(commands=['start'],
                         func=lambda msg: len(msg.text.split()) > 1)
    def startByLink(message):
        saveUser(message)
        id_to = message.text.split()[1]
        bot.send_message(message.chat.id, templateMessageStartByLink())
        bot.set_state(message.from_user.id, States.is_ready_to_send_message, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['user_from'] = int(message.chat.id)
            data['user_to'] = int(id_to)

    @bot.message_handler(content_types=['text'],
                         func=lambda msg: bot.get_state(msg.from_user.id, msg.chat.id))
    def sendText(message):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            print(data)
            saveMessageText(message, data['user_from'], data['user_to'])

            bot.send_message(data['user_from'], templateMessageFrom(message))
            bot.send_message(data['user_to'], templateMessageToWithCaption(message), parse_mode='Markdown')
        bot.delete_state(message.from_user.id, message.chat.id)

    @bot.message_handler(content_types=['sticker'],
                         func=lambda msg: bot.get_state(msg.from_user.id, msg.chat.id))
    def sendSticker(message):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            print(data)
            saveMessageSticker(message, data['user_from'], data['user_to'])

            bot.send_message(data['user_from'], templateMessageFrom(message))
            bot.send_message(data['user_to'], templateMessageTo())
            bot.send_sticker(data['user_to'], message.sticker.file_id)
        bot.delete_state(message.from_user.id, message.chat.id)

    @bot.message_handler(content_types=['photo'],
                         func=lambda msg: bot.get_state(msg.from_user.id, msg.chat.id))
    def sendPhoto(message):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            print(data)
            saveMessagePhoto(message, data['user_from'], data['user_to'])

            file_id = message.photo[-1].file_id
            file_info = bot.get_file(file_id)
            file = bot.download_file(file_info.file_path)
            with open(f'media/{file_id}.jpg', 'wb') as photo:
                photo.write(file)

            if not message.caption:
                message.caption = ''

            bot.send_message(data['user_from'], templateMessageFrom(message))
            bot.send_message(data['user_to'], templateMessageToWithCaption(message), parse_mode='Markdown')
            bot.send_photo(data['user_to'], message.photo[-1].file_id)
        bot.delete_state(message.from_user.id, message.chat.id)

    @bot.message_handler(content_types=['video'],
                         func=lambda msg: bot.get_state(msg.from_user.id, msg.chat.id))
    def sendVideo(message):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            print(data)
            saveMessageVideo(message, data['user_from'], data['user_to'])

            file_id = message.video.file_id
            file_info = bot.get_file(file_id)
            file = bot.download_file(file_info.file_path)
            with open(f'media/{file_id}.mp4', 'wb') as video:
                video.write(file)

            if not message.caption:
                message.caption = ''

            bot.send_message(data['user_from'], templateMessageFrom(message))
            bot.send_message(data['user_to'], templateMessageToWithCaption(message), parse_mode='Markdown')
            bot.send_video(data['user_to'], message.video.file_id)
        bot.delete_state(message.from_user.id, message.chat.id)

    @bot.message_handler(content_types=['voice'],
                         func=lambda msg: bot.get_state(msg.from_user.id, msg.chat.id))
    def sendVoice(message):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            print(data)
            saveMessageVoice(message, data['user_from'], data['user_to'])

            file_id = message.voice.file_id
            file_info = bot.get_file(file_id)
            file = bot.download_file(file_info.file_path)
            with open(f'media/{file_id}.mp3', 'wb') as voice:
                voice.write(file)

            bot.send_message(data['user_from'], templateMessageFrom(message))
            bot.send_message(data['user_to'], templateMessageTo())
            bot.send_voice(data['user_to'], message.voice.file_id)
        bot.delete_state(message.from_user.id, message.chat.id)

    @bot.message_handler(content_types=['video_note'],
                         func=lambda msg: bot.get_state(msg.from_user.id, msg.chat.id))
    def sendVideoNote(message):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            print(data)
            saveMessageVideoNote(message, data['user_from'], data['user_to'])

            file_id = message.video_note.file_id
            file_info = bot.get_file(file_id)
            file = bot.download_file(file_info.file_path)
            with open(f'media/{file_id}.mp4', 'wb') as video_note:
                video_note.write(file)

            bot.send_message(data['user_from'], templateMessageFrom(message))
            bot.send_message(data['user_to'], templateMessageTo())
            bot.send_video_note(data['user_to'], message.video_note.file_id)
        bot.delete_state(message.from_user.id, message.chat.id)

    bot.infinity_polling()


if __name__ == '__main__':
    main()

from django.core.management.base import BaseCommand
from django.conf import settings

import telebot

from users.models import BotConfig


class Command(BaseCommand):
    help = 'Start Telegram Bot'

    def start(self, message):
        tg_user = message.chat.username
        bot_config = BotConfig.objects.filter(tg_username=tg_user).first()
        if bot_config:
            bot_config.tg_id = message.chat.id
            bot_config.is_active = True
            bot_config.save()
            return (f'Привет, {message.chat.first_name}!\n'
                    'Вы включили рассылку сервиса V MESTE!')
        return (f'Пользователь {message.chat.username} не найден.\n'
                'Пожалуйста, проверьте профиль на сайте.')

    def stop(self, message):
        tg_user = message.chat.username
        bot_config = BotConfig.objects.filter(tg_username=tg_user).first()
        if bot_config:
            bot_config.is_active = False
            bot_config.save()
            return ('Вы отключили рассылку сервиса V MESTE.')
        return (f'Пользователь {message.chat.username} не найден.\n'
                'Пожалуйста, проверьте профиль на сайте.')

    def handle(self, *args, **kwargs):
        bot = telebot.TeleBot(token=settings.TELEGRAM_TOKEN, parse_mode=None)

        @bot.message_handler(commands=['start'])
        def start(message):
            bot.send_message(message.chat.id, self.start(message))

        @bot.message_handler(commands=['stop'])
        def stop(message):
            bot.send_message(message.chat.id, self.stop(message))

        @bot.message_handler(commands=['meetings'])
        def meetings(message):
            bot.send_message(message.chat.id, self.meetings(message))

        bot.infinity_polling()

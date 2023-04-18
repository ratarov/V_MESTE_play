import threading
import requests
from abc import abstractmethod

from django.conf import settings
from django.urls import reverse

from users.models import BotConfig


TG_URL = f'https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage'
DOMAIN = settings.DOMAIN


class InformThread(threading.Thread):
    """Абстракция для процессов по рассылке сообщений о встречах"""
    @abstractmethod
    def get_recipients(self):
        pass

    @abstractmethod
    def is_needed(self, user):
        pass

    @abstractmethod
    def get_message(self):
        pass

    def bot_is_active(self, user):
        return user.telegram and user.bot_config.is_active

    def run(self):
        for recipient in self.get_recipients():
            if self.bot_is_active(recipient) and self.is_needed(recipient):
                print(f'Отправка сообщения в телеграм {recipient.username}')
                requests.get(TG_URL, params={
                    'chat_id': recipient.bot_config.tg_id,
                    'text': self.get_message()
                })


class NewCommentInformThread(InformThread):
    """Рассылка участникам о новых комментариях к встрече"""
    def __init__(self, comment, author):
        self.comment = comment
        self.author = author
        threading.Thread.__init__(self)

    def get_recipients(self):
        return [p.player for p in self.comment.meeting.participants.
                exclude(player=self.comment.creator).
                select_related('player', 'player__bot_config')]

    def is_needed(self, user):
        return user.bot_config.comments_info

    def get_message(self):
        url_end = reverse('meetings:meeting_detail',
                          args=(self.comment.meeting.id,))
        return (f"Новое сообщение:\n"
                f"Встреча: {self.comment.meeting.get_name()} "
                f"({self.comment.meeting.start_date})\n"
                f"Игрок {self.comment.creator} написал:\n"
                f"{self.comment.text}\n"
                f"Детали: {DOMAIN}{url_end}")


class CancelMeetingInformThread(InformThread):
    """Рассылка участникам об отмене встречи"""
    def __init__(self, meeting):
        self.meeting = meeting
        threading.Thread.__init__(self)

    def get_recipients(self):
        return self.meeting.players.select_related('bot_config')

    def is_needed(self, user):
        return user.bot_config.cancel_meeting_info

    def get_message(self):
        url_end = reverse('meetings:meeting_detail', args=(self.meeting.id,))
        return (f"Ваша встреча отменена\n{self.meeting}\n"
                f"Детали: {DOMAIN}{url_end}")


class NewMeetingInformThread(InformThread):
    """Рассылка о создании новой встречи по фильтрам пользователя"""
    def __init__(self, meeting):
        self.meeting = meeting
        threading.Thread.__init__(self)

    def get_recipients(self):
        lat = self.meeting.place.loc_lat
        lon = self.meeting.place.loc_lon
        recipients = BotConfig.objects.filter(
            min_lat__lte=lat,
            max_lat__gte=lat,
            min_lon__lte=lon,
            max_lon__gte=lon,
            games__in=self.meeting.games.all(),
        )
        if self.meeting.creator.telegram:
            recipients = recipients.exclude(user=self.meeting.creator)
        return recipients

    def get_message(self):
        url_end = reverse('meetings:meeting_detail', args=(self.meeting.id,))
        return (f"Новая встреча по Вашему фильтру\n{self.meeting}\n"
                f"Детали: {DOMAIN}{url_end}")

    def run(self):
        for recipient in self.get_recipients():
            print(f'Отправка сообщения в телеграм {recipient.user.username}')
            requests.get(TG_URL, params={
                'chat_id': recipient.tg_id,
                'text': self.get_message()
            })

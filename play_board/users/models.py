from django.contrib.auth.models import AbstractUser
from django.db import models
from geopy.geocoders import Nominatim
from games.models import Game
from django import forms

from users.validators import username_validator


class BotConfig(models.Model):
    RADIUS_CHOICES = ((50, 50), (20, 20), (10, 10))
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    tg_username = models.CharField(
        verbose_name='Telegram username',
        max_length=50,
    )
    tg_id = models.IntegerField(
        verbose_name='ID пользователя',
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(
        verbose_name='Включить рассылки',
        default=False
    )
    comments_info = models.BooleanField(
        verbose_name='Новые сообщения',
        default=False,
    )
    cancel_meeting_info = models.BooleanField(
        verbose_name='Отмена встречи',
        default=False,
    )
    new_meeting_info = models.BooleanField(
        verbose_name='Новые встречи',
        default=False,
    )
    address = models.CharField(
        verbose_name='Адрес для поиска',
        max_length=150,
        blank=True,
    )
    radius = models.PositiveSmallIntegerField(
        verbose_name='Радиус поиска',
        choices=RADIUS_CHOICES,
        default=50,
    )
    games = models.ManyToManyField(
        Game,
        blank=True,
    )
    loc_lat = models.DecimalField(
        verbose_name='Широта координаты центра поиска',
        blank=True, null=True,
        max_digits=9, decimal_places=6,
    )
    loc_lon = models.DecimalField(
        verbose_name='Долгота координаты центра поиска',
        blank=True, null=True,
        max_digits=9, decimal_places=6
    )
    min_lat = models.DecimalField(
        verbose_name='Мин.граница по широте',
        blank=True, null=True,
        max_digits=9, decimal_places=6,
    )
    max_lat = models.DecimalField(
        verbose_name='Макс.граница по широте',
        blank=True, null=True,
        max_digits=9, decimal_places=6,
    )
    min_lon = models.DecimalField(
        verbose_name='Мин.граница по долготе',
        blank=True, null=True,
        max_digits=9, decimal_places=6,
    )
    max_lon = models.DecimalField(
        verbose_name='Макс.граница по широте',
        blank=True, null=True,
        max_digits=9, decimal_places=6,
    )

    class Meta:
        default_related_name = 'bot_config'

    def __str__(self):
        return f'Бот для {self.user}'


class User(AbstractUser):
    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        help_text='Обязательное поле: до 50 символов, буквы, цифры, _ и -',
        validators=[username_validator],
        error_messages={
            'unique': "Такой пользователь уже существует",
        },
    )
    photo = models.ImageField(
        verbose_name='Фото',
        help_text='Можете загрузить Ваше фото',
        upload_to='photos/%Y-%m-%d',
        null=True, blank=True,
    )
    country = models.CharField(
        verbose_name='Страна проживания',
        help_text='Реальная страна для удобства поиска',
        max_length=50,
        blank=True,
    )
    city = models.CharField(
        verbose_name='Город проживания',
        help_text='Реальный город для удобства поиска',
        max_length=100,
        blank=True,
    )
    telegram = models.CharField(
        verbose_name='Телеграм аккаунт',
        help_text='Для связи с игроками и уведомлений',
        max_length=50,
        blank=True,
    )
    about = models.TextField(
        verbose_name='О себе',
        help_text='Расскажите о себе, своих увлечениях и опыте в играх',
        blank=True,
    )
    bgg_account = models.CharField(
        verbose_name='BGG ник',
        help_text='Аккаунт на boardgamegeek.com',
        max_length=50,
        blank=True,
    )
    tesera_account = models.CharField(
        verbose_name='Tesera ник',
        help_text='Аккаунт на tesera.ru',
        max_length=50,
        blank=True,
    )
    liked_games = models.ManyToManyField(
        Game,
        related_name='liked',
    )
    site_collection = models.ManyToManyField(
        Game,
        related_name='collected',
    )
    tesera_collection = models.ManyToManyField(
        Game,
        related_name='t_collected',
    )

    def __str__(self):
        return self.username

    def save(self, **kwargs):
        """Создание экземпляра модели с настройками телеграм-бота"""
        if self.telegram:
            tg_username = (self.telegram if not self.telegram.startswith('@')
                           else self.telegram[1:])
            bot_config, _ = BotConfig.objects.get_or_create(
                user=self,
                defaults={'tg_username': tg_username},
            )
            print(bot_config.tg_username)
            print(tg_username)
            if bot_config.tg_username != tg_username:
                bot_config.tg_username = tg_username
                bot_config.save()
        super(User, self).save()


class PlaceType(models.Model):
    logo = models.ImageField(
        verbose_name='Иконка',
        upload_to='icons',
        null=True, blank=True,
    )
    name = models.CharField(
        verbose_name='Название типа',
        max_length=30,
    )

    class Meta:
        verbose_name = 'Тип мест'
        verbose_name_plural = 'Типы мест'

    def __str__(self):
        return self.name


class Place(models.Model):
    type = models.ForeignKey(
        PlaceType,
        on_delete=models.SET_NULL,
        null=True,
    )
    name = models.CharField(max_length=30)
    creator = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
    )
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    building = models.CharField(max_length=10)
    flat = models.CharField(max_length=10, blank=True)
    loc_lat = models.DecimalField(
        blank=True, null=True,
        max_digits=9, decimal_places=6,
    )
    loc_lon = models.DecimalField(
        blank=True, null=True,
        max_digits=9, decimal_places=6,
    )
    comments = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'
        ordering = ('name',)
        default_related_name = 'places'

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        """Получение координат места по API Nominatim при сохранении объекта"""
        if self.address:
            try:
                geolocator = Nominatim(user_agent="Tester")
                full_address = f'{self.city}, {self.address} {self.building}'
                location = geolocator.geocode(full_address)
                self.loc_lat = location.latitude
                self.loc_lon = location.longitude
            except Exception:
                raise forms.ValidationError('Адрес не найден, введите другой')
        super(Place, self).save()

    def get_info(self):
        if self.type.name == 'квартира/дом':
            return f'{self.address}, {self.building}'
        else:
            return f'"{self.name}": {self.address}, {self.building}'

    def get_name(self):
        if self.type.name == 'квартира/дом':
            return 'Квартира/дом'
        else:
            return self.name

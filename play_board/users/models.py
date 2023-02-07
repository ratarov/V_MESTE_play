from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from geopy.geocoders import Nominatim
from games.models import Game
from django import forms


class User(AbstractUser):
    photo = models.ImageField(
        'Фото', help_text='Можете загрузить Ваше фото',
        upload_to='photos/', null=True, blank=True)
    country = models.CharField(
        'Страна проживания', help_text='Реальная страна для удобства поиска',
        max_length=50, null=True, blank=True)
    city = models.CharField(
        'Город проживания', help_text='Реальный город для удобства поиска',
        max_length=100, null=True, blank=True)
    telegram = models.CharField(
        'Телеграм аккаунт', help_text='Для связи с игроками и уведомлений',
        max_length=50, null=True, blank=True)
    about = models.TextField(
        'О себе',
        help_text='Расскажите о себе, своих увлечениях и опыте в играх',
        null=True, blank=True)
    bgg_account = models.CharField(
        'BGG ник', help_text='Имя пользователя на boardgamegeek.com',
        max_length=50, null=True, blank=True)
    tesera_account = models.CharField(
        'Tesera ник', help_text='Имя пользователя на tesera.ru',
        max_length=50, null=True, blank=True)
    liked_games = models.ManyToManyField(
        Game, related_name='liked_games')
    site_collection = models.ManyToManyField(
        Game, related_name='site_collection')
    tesera_collection = models.ManyToManyField(
        Game, related_name='tesera_collection')


class PlaceType(models.Model):
    logo = models.ImageField('Иконка', upload_to='icons', 
                             null=True, blank=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Place(models.Model):
    type = models.ForeignKey(PlaceType, on_delete=models.SET_NULL,
                             null=True)
    name = models.CharField(max_length=30)
    creator = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    building = models.CharField(max_length=10)
    flat = models.CharField(max_length=10, blank=True, null=True)
    loc_lat = models.DecimalField(
        blank=True, null=True, max_digits=9, decimal_places=6)
    loc_lon = models.DecimalField(
        blank=True, null=True, max_digits=9, decimal_places=6)
    comments = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'
        ordering = ('name',)
        default_related_name = 'places'
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=['creator', 'name'],
        #         name='unique_gamer_place'
        #     )
        # ]

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        if self.address:
            try:
                geolocator = Nominatim(user_agent="Tester")
                full_address = f'{self.city} {self.address} {self.building}'
                location = geolocator.geocode(full_address)
                self.loc_lat = location.latitude
                self.loc_lon = location.longitude
                super(Place, self).save()
            except Exception:
                raise forms.ValidationError('Адрес не найден, введите другой')
        super(Place, self).save()

    def get_info(self):
        if self.type.name == 'квартира/дом':
            return self.address
        else:
            return f'"{self.name}": {self.address}, {self.building}'

    def get_name(self):
        if self.type.name == 'квартира/дом':
            return 'Квартира/дом'
        else:
            return self.name
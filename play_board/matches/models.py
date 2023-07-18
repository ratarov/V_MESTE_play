from django.db import models

from games.models import Game
from users.models import User


class Match(models.Model):
    class Type(models.TextChoices):
        PvP = 'PvP', 'Игрок vs Игрока'
        PvG = 'PvG', 'Игрок vs Игры'

    class Status(models.TextChoices):
        DRAFT = 'draft', 'черновик'
        IGNORE = 'ignore', 'пропуск'
        OK = 'ok', 'ок'

    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    game = models.ForeignKey(Game, on_delete=models.PROTECT, null=True)
    place = models.CharField(max_length=50, default='квартира/дом')
    type = models.CharField(max_length=20, choices=Type.choices, default=Type.PvP)
    quantity = models.PositiveSmallIntegerField(default=1)
    length = models.PositiveSmallIntegerField(blank=True, null=True)
    comments = models.TextField(blank=True)
    ignore = models.BooleanField(default=True)
    incomplete = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)

    class Meta:
        ordering = ('-date',)
        verbose_name = 'Партия'
        verbose_name_plural = 'Партии'

    def __str__(self):
        return f'{self.date} партия {self.creator} в {self.game}'


class Player(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='players', null=True)
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='played')
    username = models.TextField()
    team = models.CharField(max_length=50, blank=True)
    start_position = models.CharField(max_length=50, blank=True)
    score = models.PositiveSmallIntegerField(blank=True, null=True)
    winner = models.BooleanField(default=False)

    class Meta:
        ordering = ('-winner', 'name')
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'

    def __str__(self):
        return f'{self.name} {self.user}'

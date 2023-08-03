from django.db import models

from games.models import Game
from users.models import User, Place


class Match(models.Model):
    """Модель партии."""
    class Type(models.TextChoices):
        PvP = 'PvP', 'Игрок vs Игрока'
        PvG = 'PvG', 'Игрок vs Игры'
        SOLO = 'solo', 'Соло'

    class Status(models.TextChoices):
        DRAFT = 'draft', 'черновик'
        IGNORE = 'ignore', 'незачёт'
        OK = 'ok', 'зачёт'

    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Создатель партии',
    )
    date = models.DateField(verbose_name='Дата партии')
    game = models.ForeignKey(
        Game,
        on_delete=models.PROTECT,
        null=True,
        verbose_name='Игра',
        related_name='matches',
    )
    place = models.ForeignKey(
        Place,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Место игры',
        related_name='matches',
    )
    type = models.CharField(
        verbose_name='Тип игры',
        max_length=20,
        choices=Type.choices,
        default=Type.PvP,
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Кол-во партий',
        default=1,
    )
    length = models.PositiveSmallIntegerField(
        verbose_name='Длительность партии, мин',
        blank=True,
        null=True,
    )
    comments = models.TextField(verbose_name='Комментарии', blank=True)
    ignore = models.BooleanField(
        verbose_name='Не учитывать в общем зачете',
        default=False,
    )
    incomplete = models.BooleanField(verbose_name='Не доиграли', default=False)
    status = models.CharField(
        verbose_name='Статус партии',
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    class Meta:
        ordering = ('-date',)
        verbose_name = 'Партия'
        verbose_name_plural = 'Партии'

    def __str__(self):
        return f'{self.date} партия {self.creator} в {self.game}'


class Player(models.Model):
    """Модель игрока в партии"""
    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        related_name='players',
        null=True,
        verbose_name='Партия',
    )
    name = models.CharField(
        verbose_name='Имя',
        max_length=50,
        blank=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='played',
        verbose_name='Пользователь',
    )
    username = models.CharField(verbose_name='Ник', max_length=100)
    team = models.CharField(
        verbose_name='Имя команды',
        max_length=50,
        blank=True,
    )
    start_position = models.CharField(
        verbose_name='Начальная позиция',
        max_length=50,
        blank=True,
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Кол-во очков',
        blank=True,
        null=True,
    )
    winner = models.BooleanField(
        verbose_name='Флаг победителя',
        default=False,
    )

    class Meta:
        ordering = ('-winner', 'name')
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'

    def __str__(self):
        return f'Игрок {self.name} {self.user}'

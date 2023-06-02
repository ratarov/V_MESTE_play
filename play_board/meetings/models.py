from django.db import models
from users.models import User, Place
from games.models import Game


class MeetingStatus(models.Model):
    logo = models.ImageField('Иконка', upload_to='icons',
                             null=True, blank=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Meeting(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=50,
        blank=True,
    )
    status = models.ForeignKey(
        MeetingStatus,
        default=1,
        on_delete=models.SET_DEFAULT,
    )
    games = models.ManyToManyField(
        Game,
        blank=True,
    )
    start_date = models.DateField(verbose_name='Дата встречи')
    start_time = models.TimeField(verbose_name='Время встречи')
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created',
    )
    guests = models.PositiveSmallIntegerField(
        verbose_name='Гости организатора',
        default=0,
    )
    players = models.ManyToManyField(
        User, through='MeetingParticipation',
        blank=True,
    )
    max_players = models.PositiveSmallIntegerField(
        verbose_name='Максимальное кол-во игроков',
        default=7,
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
    )
    price = models.PositiveIntegerField(
        verbose_name='Цена участия',
        default=0,
    )
    place = models.ForeignKey(
        Place, null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = 'Встреча'
        verbose_name_plural = 'Встречи'
        ordering = ('start_date',)
        default_related_name = 'meetings'

    def __str__(self):
        if self.name:
            return f'{self.start_date}: {self.name}'
        return f'{self.start_date}: Настолки с {self.creator}'

    def get_active_players(self):
        return MeetingParticipation.objects.filter(
            meeting=self, status='ACT'
        ).select_related('player')

    def get_banned_players(self):
        return MeetingParticipation.objects.filter(
            meeting=self, status='BAN'
        ).select_related('player')

    def get_total_players(self):
        return sum(self.participants.values_list('total_qty', flat=True))

    def get_price(self):
        return self.price or 'бесплатно'

    def get_name(self):
        return self.name or f'Настолки с {self.creator.username}'


class MeetingParticipation(models.Model):
    STATUS_CHOICE = (
        ('ACT', 'active'),
        ('BAN', 'banned'),
    )
    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.CASCADE,
        related_name='participants',
    )
    player = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='participated',
    )
    guests = models.PositiveSmallIntegerField(
        verbose_name='Количество гостей',
        default=0,
    )
    status = models.CharField(
        verbose_name='Статус участника',
        max_length=20,
        choices=STATUS_CHOICE,
        default='ACT'
    )
    total_qty = models.PositiveSmallIntegerField(
        verbose_name='Игрок + гости',
    )

    class Meta:
        verbose_name = 'Участник встречи'
        verbose_name_plural = 'Участники встречи'
        constraints = [
            models.UniqueConstraint(
                fields=['meeting', 'player'],
                name='unique_participant'
            )
        ]

    def __str__(self):
        return f'{self.player.username} + {self.guests}'

    def save(self, **kwargs):
        if self.status == 'ACT':
            self.total_qty = 1 + int(self.guests)
        else:
            self.total_qty = 0
        super(MeetingParticipation, self).save()


class Comment(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=300)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created',)
        default_related_name = 'comments'

    def __str__(self):
        return self.text[:15]

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
        'Название', max_length=30, blank=True, null=True)
    status = models.ForeignKey(
        MeetingStatus, related_name='meetings', default=1, on_delete=models.SET_DEFAULT)
    games = models.ManyToManyField(
        Game, blank=True, related_name='meetings')
    start_date = models.DateField('Дата встречи')
    start_time = models.TimeField('Время встречи')
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='meetings')
    guests = models.PositiveSmallIntegerField(
        'Гости организатора', default=0)
    players = models.ManyToManyField(
        User, blank=True,
        through='MeetingParticipation', related_name='played')
    max_players = models.PositiveSmallIntegerField(
        'Максимальное кол-во игроков', default=7)
    description = models.TextField(blank=True, null=True)
    price = models.PositiveIntegerField(default=0)
    place = models.ForeignKey(
        Place, null=True, on_delete=models.SET_NULL,
        related_name='meetings')

    class Meta:
        verbose_name = 'Встреча'
        verbose_name_plural = 'Встречи'
        ordering = ('start_date', 'start_time')

    def __str__(self):
        return f'{self.start_date} - {self.creator} - {self.place}'

    def get_active_players(self):
        return MeetingParticipation.objects.filter(meeting=self, status='ACT')

    def get_banned_players(self):
        return MeetingParticipation.objects.filter(meeting=self, status='BAN')

    def get_total_players(self):
        players_qty = self.participants.filter(status='ACT').count()
        guests_qty = self.participants.filter(status='ACT').values_list('guests', flat=True)
        return sum(guests_qty) + players_qty

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
        Meeting, on_delete=models.CASCADE,
        related_name='participants')
    player = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='participated')
    guests = models.PositiveSmallIntegerField(
        'Количество гостей', default=0)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICE, default='ACT')

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

    def get_player_with_guests(self):
        return (self.guests + 1)


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
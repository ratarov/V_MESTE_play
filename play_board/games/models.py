from django.db import models


class Game(models.Model):
    tesera_id = models.PositiveIntegerField(null=True)
    bgg_id = models.PositiveIntegerField(null=True)
    name_rus = models.CharField(max_length=255, null=True)
    name_eng = models.CharField(max_length=255, null=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True)
    photo_url = models.URLField(null=True)
    year = models.IntegerField(null=True)
    players_min = models.PositiveSmallIntegerField(null=True)
    players_max = models.PositiveSmallIntegerField(null=True)
    duration_min = models.PositiveSmallIntegerField(null=True)
    duration_max = models.PositiveSmallIntegerField(null=True)
    age = models.IntegerField(null=True)
    time_to_learn = models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        return self.name_rus or self.name_eng

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'
        ordering = ('name_rus',)

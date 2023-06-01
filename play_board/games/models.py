from django.db import models


class Game(models.Model):
    tesera_id = models.PositiveIntegerField(null=True, blank=True)
    bgg_id = models.PositiveIntegerField(null=True, blank=True)
    name_rus = models.CharField(max_length=255)
    name_eng = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=100)
    description = models.TextField(null=True, blank=True)
    photo_url = models.URLField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    players_min = models.PositiveSmallIntegerField(null=True, blank=True)
    players_max = models.PositiveSmallIntegerField(null=True, blank=True)
    duration_min = models.PositiveSmallIntegerField(null=True, blank=True)
    duration_max = models.PositiveSmallIntegerField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    time_to_learn = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name_rus or self.name_eng

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'
        ordering = ('name_rus',)

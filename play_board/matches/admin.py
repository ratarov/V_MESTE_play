from django.contrib import admin

from .models import Match, Player


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'creator',
        'date',
        'game',
        'place',
        'status',
    )


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'match',
        'name',
        'user',
        'score',
        'winner',
    )

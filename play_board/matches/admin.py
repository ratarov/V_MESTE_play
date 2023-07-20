from django.contrib import admin

from .models import Match, Player


class PlayerAdmin(admin.TabularInline):
    model = Player
    fields = ('id', 'name', 'user', 'team', 'score', 'winner')


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    inlines = (PlayerAdmin,)
    list_display = (
        'id',
        'creator',
        'date',
        'game',
        'place',
        'status',
    )

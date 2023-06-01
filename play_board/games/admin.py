from django.contrib import admin
from games.models import Game


class GameAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name_rus',
        'name_eng',
        'slug',
        'year',
    )
    search_fields = ['name_rus', 'name_eng']


admin.site.register(Game, GameAdmin)

from django.contrib import admin

from .models import Game


class GameAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name_rus',
        'name_eng',
        'slug',
        'year',
    )
    search_fields = ['name_rus', 'name_eng', 'slug']


admin.site.register(Game, GameAdmin)

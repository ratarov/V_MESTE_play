from django.contrib import admin
from games.models import Game


class GameAdmin(admin.ModelAdmin):
    search_fields = ['name_rus']


admin.site.register(Game, GameAdmin)
from django.contrib import admin

from .models import Place, PlaceType, User, BotConfig


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'country',
        'city',
    )
    search_fields = ('username',)
    autocomplete_fields = ['liked_games', 'site_collection',
                           'tesera_collection']
    empty_value_display = '-пусто-'


class BotConfigAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'tg_username',
        'tg_id',
        'is_active',
    )
    search_fields = ('user', 'tg_username')
    autocomplete_fields = ['games']
    empty_value_display = '-пусто-'


class PlaceAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'creator',
        'city',
        'address',
        'building',
    )
    search_fields = ('creator', 'name')
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.register(BotConfig, BotConfigAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(PlaceType)

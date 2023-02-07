from django.contrib import admin

from .models import Place, PlaceType, User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'first_name',
        'last_name',
        'country',
        'city',
    )
    search_fields = ('username',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.register(Place)
admin.site.register(PlaceType)

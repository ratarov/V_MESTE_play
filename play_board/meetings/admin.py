from django.contrib import admin
from meetings.models import (Comment, Meeting, MeetingStatus,
                             MeetingParticipation)


class MeetingAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'status',
        'start_date',
        'creator',
        'max_players',
        'place',
    )
    search_fields = ['games']
    autocomplete_fields = ['games']
    empty_value_display = '-пусто-'


admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Comment)
admin.site.register(MeetingStatus)
admin.site.register(MeetingParticipation)

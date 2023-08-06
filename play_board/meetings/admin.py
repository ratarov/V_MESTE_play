from django.contrib import admin

from .models import (Comment, Meeting, MeetingStatus,
                     MeetingParticipation)


class ParticipationAdmin(admin.TabularInline):
    model = MeetingParticipation


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    inlines = (ParticipationAdmin,)
    list_display = (
        'id',
        'status',
        'start_date',
        'creator',
        'max_players',
        'place',
    )
    search_fields = ['games']
    autocomplete_fields = ['games']
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'creator',
        'created',
        'meeting',
        'text',
    )


@admin.register(MeetingParticipation)
class MeetingParticipationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'meeting',
        'player',
        'guests',
        'status',
    )


@admin.register(MeetingStatus)
class MeetingStatusAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name'
    )

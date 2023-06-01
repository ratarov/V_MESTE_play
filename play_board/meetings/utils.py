from math import cos, pi

import folium
from django.conf import settings
from django.db.models import Sum
from django.urls import reverse
from django.utils import timezone

from meetings.models import Meeting


def filter_meetings(place, request):
    """Фильтрация queryset Meeting по заданным фильтрам"""
    radius = int(request.GET.get('radius', settings.DEFAULT_SEARCH_RADIUS))
    latitude_diff = radius / settings.KM_IN_DEGREE
    longitude_diff = radius / (
        cos(place.latitude / 180 * pi) * settings.KM_IN_DEGREE
    )
    date_since = request.GET.get('date_since')
    date_until = request.GET.get('date_until')
    game = request.GET.get('game')
    meetings = Meeting.objects.filter(
        start_date__gte=timezone.now(),
        status_id=1,
        place__loc_lat__gt=(place.latitude - latitude_diff),
        place__loc_lat__lt=(place.latitude + latitude_diff),
        place__loc_lon__gt=(place.longitude - longitude_diff),
        place__loc_lon__lt=(place.longitude + longitude_diff),
    )
    if date_since:
        meetings = meetings.filter(start_date__gte=date_since)
    if date_until:
        meetings = meetings.filter(start_date__lte=date_until)
    if game:
        meetings = meetings.filter(games__id=game)
    if request.user.is_authenticated:
        meetings = meetings.exclude(creator=request.user)
    return (meetings.
            select_related('status', 'creator', 'place', 'place__type').
            prefetch_related('games').
            annotate(total_players=Sum('participants__total_qty')).
            order_by('start_date'))


def add_meeting_marker(map, meeting):
    """Добавление маркера встречи на карту Folium"""
    games = ', '.join([str(x) for x in list(meeting.games.all()[:3])])
    url = reverse('meetings:meeting_detail', args=(meeting.id,))
    html = f'''
        <b>Дата: </b>
        <a href="{url}" target="_top">
            {meeting.start_date}
        </a>
        <br>
        <b>Команда:</b> {meeting.total_players}/{meeting.max_players}
        <br>
        <b>Игры:</b> {games}
    '''
    text = f'<b>{meeting.get_name()}</b><br><b>Игры:</b> {games}'
    folium.Marker(
        location=[meeting.place.loc_lat, meeting.place.loc_lon],
        popup=folium.Popup(html, max_width=120),
        tooltip=folium.Tooltip(text),
    ).add_to(map)
    return map

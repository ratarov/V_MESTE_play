from django.shortcuts import redirect
from django.utils import timezone
from geopy.geocoders import Nominatim
from meetings.models import Meeting
from django.conf import settings
import folium
from django.urls import reverse
from django.db.models import Sum


def get_geolocation(location):
    """Получение геопозиции по адресу"""
    try:
        geolocator = Nominatim(user_agent="Tester")
        geolocation = geolocator.geocode(location)
    except Exception:
        print('Ошибка доступа к сервису геолокации')
        return redirect('meetings:meeting_search')
    return geolocation


def filter_meetings(place, request):
    """Фильтрация queryset Meeting по заданным фильтрам"""
    radius = int(request.GET.get('radius', settings.DEFAULT_SEARCH_RADIUS))
    dist_diff = radius / settings.KM_IN_DEGREE
    date_since = request.GET.get('date_since')
    date_until = request.GET.get('date_until')
    game = request.GET.get('game')
    meetings = Meeting.objects.filter(
        start_date__gte=timezone.now(),
        status_id=1,
        place__loc_lat__gt=(place.latitude - dist_diff),
        place__loc_lat__lt=(place.latitude + dist_diff),
        place__loc_lon__gt=(place.longitude - dist_diff),
        place__loc_lon__lt=(place.longitude + dist_diff),
    )
    if date_since:
        meetings = meetings.filter(start_date__gte=date_since)
    if date_until:
        meetings = meetings.filter(start_date__lte=date_until)
    if game:
        meetings = meetings.filter(games__id=game)
    if request.user.is_authenticated:
        meetings = meetings.exclude(creator=request.user)
    return meetings.select_related(
            'status', 'creator', 'place', 'place__type',
        ).prefetch_related('games').annotate(
            total_players=Sum('participants__total_qty')
        )


def add_meeting_marker(map, meeting):
    """Добавление маркера встречи на карту Folium"""
    games = ','.join(meeting.games.values_list('name_rus', flat=True)[:3])
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

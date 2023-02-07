from django.shortcuts import render, redirect
from django.utils import timezone
from geopy.geocoders import Nominatim
from meetings.forms import CommentForm, MeetingForm, MeetingSearchForm
from meetings.models import Comment, Meeting, MeetingStatus
from django.conf import settings
import folium
from django.urls import reverse


def get_geolocation(location):
    try:
        geolocator = Nominatim(user_agent="Tester")
        geolocation = geolocator.geocode(location)
    except Exception:
        print('Ошибка доступа к сервису геолокации')
        return redirect('meetings:meeting_search')
    return geolocation


def filter_meetings(place, request):
    radius = int(request.GET.get('radius'))
    date_since = request.GET.get('date_since')
    date_until = request.GET.get('date_until')
    game = request.GET.get('game')
    meetings = Meeting.objects.filter(
        start_date__gte=timezone.now(),
        status__name='готовится',
        place__loc_lat__gt=(place.latitude - radius / settings.KM_IN_DEGREE),
        place__loc_lat__lt=(place.latitude + radius / settings.KM_IN_DEGREE),
        place__loc_lon__gt=(place.longitude - radius / settings.KM_IN_DEGREE),
        place__loc_lon__lt=(place.longitude + radius / settings.KM_IN_DEGREE),
    )
    if date_since:
        meetings = meetings.filter(start_date__gte=date_since)
    if date_until:
        meetings = meetings.filter(start_date__lte=date_until)
    if game:
        meetings = meetings.filter(games__id=game)
    return meetings


def add_meeting_marker(map, meeting):
    games = ','.join(meeting.games.values_list('name_rus', flat=True)[:3])
    url = reverse('meetings:meeting_detail', args=(meeting.id,))
    html = f'''
        <b>Дата: </b>
        <a href="{url}" target="_top">
            {meeting.start_date}
        </a>
        <br>
        <b>Команда:</b> {meeting.get_total_players()}/{meeting.max_players}
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

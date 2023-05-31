import requests

import folium
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Sum


USER_DETAIL_URL = 'https://api.tesera.ru/user/'
COLLECTION_URL = 'https://api.tesera.ru/collections/base/own/'


def get_tesera_user(tesera_account):
    """Получение данных пользователя по нику с сайта tesera.ru"""
    try:
        request = requests.get(f'{USER_DETAIL_URL}{tesera_account}/').json()
    except Exception:
        print(f'Ошибка при запросе инфо игрока {tesera_account}')
    if request:
        return int(request.get('gamesInCollection'))
    return 0


def get_tesera_collection(tesera_account, games_in_col):
    """Получение данных о коллекции игрока с сайта tesera.ru"""
    try:
        return requests.get(
            f'{COLLECTION_URL}{tesera_account}/?limit={games_in_col}').json()
    except Exception:
        print(f'Ошибка при запросе коллекции игрока {tesera_account}')


def get_paginated_games(queryset, request):
    """Пагинация списка игр"""
    paginator = Paginator(queryset, settings.GAMES_ON_PAGE)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def filter_user_meetings(request):
    """Фильтрация списка встреч пользователя"""
    status = request.GET.get('status')
    host = request.GET.get('host')
    date_since = request.GET.get('date_since')
    date_until = request.GET.get('date_until')
    meetings = (
        request.user.meetings.
        order_by('-start_date').
        select_related('creator', 'place', 'status', 'place__type').
        prefetch_related('games').
        annotate(total_players=Sum('participants__total_qty'))
    )
    if status:
        meetings = meetings.filter(status__name=status)
    if host:
        if host == 'Вы':
            meetings = meetings.filter(creator=request.user)
        else:
            meetings = meetings.exclude(creator=request.user)
    if date_since:
        meetings = meetings.filter(start_date__gte=date_since)
    if date_until:
        return meetings.filter(start_date__lte=date_until)
    return meetings


def add_search_marker(map, bot_config):
    """Добавление маркера поиска на карту Folium"""
    text = 'Точка отсчета для поиска'
    folium.Marker(
        location=[bot_config.loc_lat, bot_config.loc_lon],
        tooltip=folium.Tooltip(text),
    ).add_to(map)
    return map

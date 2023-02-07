import requests
from django.conf import settings
from django.core.paginator import Paginator

USER_DETAIL_URL = 'https://api.tesera.ru/user/'
COLLECTION_URL = 'https://api.tesera.ru/collections/base/own/'


def get_tesera_user(tesera_account):
    try:
        request = requests.get(f'{USER_DETAIL_URL}{tesera_account}/').json()
    except Exception:
        print(f'Ошибка при запросе инфо игрока {tesera_account}')
    if request:
        games_in_col = int(request.get('gamesInCollection'))
        return games_in_col
    return 0


def get_tesera_collection(tesera_account, games_in_col):
    try:
        return requests.get(
            f'{COLLECTION_URL}{tesera_account}/?limit={games_in_col}').json()
    except Exception:
        print(f'Ошибка при запросе коллекции игрока {tesera_account}')


def get_paginated_games(queryset, request):
    paginator = Paginator(queryset, settings.GAMES_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj

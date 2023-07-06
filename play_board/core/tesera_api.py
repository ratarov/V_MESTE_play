import logging
from http import HTTPStatus

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

TIMEOUT = 2
COLLECTION_URL = 'https://api.tesera.ru/collections/base/own/'
GAME_SEARCH_URL = 'https://api.tesera.ru/search/games?query='
GAME_DETAIL_URL = 'https://api.tesera.ru/games/'
FIELDS = {
    'teseraId': 'tesera_id',
    'bggId': 'bgg_id',
    'title': 'name_rus',
    'title2': 'name_eng',
    'alias': 'slug',
    'description': 'description',
    'photoUrl': 'photo_url',
    'year': 'year',
    'playersMin': 'players_min',
    'playersMax': 'players_max',
    'playtimeMin': 'duration_min',
    'playtimeMax': 'duration_max',
    'playersAgeMin': 'age',
    'timeToLearn': 'time_to_learn',
}


def search_games(name):
    """Получение ответа на запрос с поиском игры от сайта tesera.ru"""
    try:
        r = requests.get(f'{GAME_SEARCH_URL}{name}', timeout=TIMEOUT).json()
        return r
    except requests.exceptions.Timeout:
        logger.error('Вышло время ожидания ответ от api.tesera.ru')
    except Exception:
        logger.error('Неожиданная ошибка при поиски игры на tesera.ru')
    return []


def parse_tesera_response(tesera_response):
    """Парсинг ответа tesera со списком игр"""
    all_games_data = []
    for data_set in tesera_response:
        game_data = {}
        for field in FIELDS:
            if 'relationId' in data_set:
                game_data[FIELDS[field]] = data_set.get('game').get(field)
            else:
                game_data[FIELDS[field]] = data_set.get(field)
        all_games_data.append(game_data)
    return all_games_data


def update_game_data(game):
    """Обновление данных об игре при заходе на страницу игры (если надо)"""
    try:
        request = requests.get(
            f'{GAME_DETAIL_URL}{game.slug}', timeout=TIMEOUT
        ).json().get('game')
        game.bgg_id = request.get('bggId')
        game.name_eng = (request.get('title2') if request.get('title2')
                         else request.get('title3'))
        game.description = request.get('description')
        game.year = request.get('year')
        game.players_min = request.get('playersMin')
        game.players_max = request.get('playersMax')
        game.duration_min = request.get('playtimeMin')
        game.duration_max = request.get('playtimeMax')
        game.age = request.get('playersAgeMin')
        game.time_to_learn = request.get('timeToLearn')
        game.save(update_fields=['bgg_id', 'name_eng', 'description', 'year',
                                 'players_min', 'players_max', 'duration_min',
                                 'duration_max', 'age', 'time_to_learn'])
        logger.info(f'Игра {game.slug} обновлена')
    except requests.exceptions.Timeout:
        logger.error('Вышло время ожидания ответ от api.tesera.ru')
    except Exception:
        logger.error(f'Ошибка при запросе игры {game.slug} на tesera.ru')


def get_tesera_collection(tesera_account):
    """Получение данных о коллекции игрока с сайта tesera.ru"""
    try:
        raw_games = []
        offset, limit = 0, settings.TESERA_GAMES_IN_REQUEST
        while True:
            response = requests.get(
                (f'{COLLECTION_URL}{tesera_account}/'
                 f'?offset={offset}&limit={limit}'),
                timeout=TIMEOUT
            )
            if response.status_code != HTTPStatus.OK:
                logger.error(f'Статус от tesera.ru {response.status_code}')
                break
            collection_size = int(response.headers.get('X-Total-Count', 0))
            games_batch = response.json()
            raw_games.extend(games_batch)
            offset += 1
            if limit * (offset) >= collection_size:
                break
        return raw_games
    except requests.exceptions.Timeout:
        logger.error('Истек срок ответа api.tesera.ru')
    except Exception:
        logger.error(f'Ошибка при запросе коллекции игрока {tesera_account}')
    return []

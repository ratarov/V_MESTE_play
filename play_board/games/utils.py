import requests
from games.models import Game


SEARCH_URL = 'https://api.tesera.ru/search/games?query='
DETAIL_URL = 'https://api.tesera.ru/games/'
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
        return requests.get(f'{SEARCH_URL}{name}').json()
    except Exception:
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
        request = requests.get(f'{DETAIL_URL}{game.slug}').json().get('game')
        game.bgg_id = request.get('bggId')
        game.name_eng = request.get('title2', 'title3')
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
        print(f'Игра {game.slug} обновлена')
    except Exception:
        print(f'Ошибка при запросе игры {game.slug} на tesera.ru')


def create_game(dataset):
    """Создание игры"""
    slug = dataset['slug']
    try:
        Game.objects.create(
            tesera_id=dataset['tesera_id'],
            bgg_id=dataset['bgg_id'],
            name_rus=dataset['name_rus'],
            name_eng=dataset['name_eng'],
            slug=dataset['slug'],
            description=dataset['description'],
            photo_url=dataset['photo_url'],
            year=dataset['year'],
            players_min=dataset['players_min'],
            players_max=dataset['players_max'],
            duration_min=dataset['duration_min'],
            duration_max=dataset['duration_max'],
            age=dataset['age'],
            time_to_learn=dataset['time_to_learn'],
        )
    except Exception:
        print(f'Ошибка при создании игры {slug}')
    print(f'Создана игра {slug}')

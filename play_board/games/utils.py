# from bs4 import BeautifulSoup
import requests
from games.models import Game

TOP_GAMES = [
    'Gloomhaven (Мрачная гавань)',
    'Брасс. Бирмингем',
    'Пандемия. Наследие: cезон первый',
    'Покорение Марса',
    'Сумерки империи. Четвёртая редакция'
]
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
    try:
        return requests.get(f'{SEARCH_URL}{name}').json()
    except Exception:
        return []


def parse_tesera_response(tesera_response):
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
    try:
        request = requests.get(f'{DETAIL_URL}{game.slug}').json().get('game')
    except Exception:
        print(f'Ошибка при запросе игры {game.slug} на tesera.ru')
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


def create_game(dataset):
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


# db = []
# slugs = search_games('санкт-петербург')
# print(f'slugs: {slugs}')
# if slugs:
#     new = get_games_details(slugs, db)
#     print(f'new games: {new}')


# def get_top600():
#     TOP_GAMES_URL = 'https://nastolki-spb.ru/ranks'
#     r = requests.get(TOP_GAMES_URL)
#     soup = BeautifulSoup(r.text, 'html.parser')
#     games = soup.findAll('td', class_='rait-tit')
#     listforbd = []
#     for game in games:
#         a = str(game)
#         b = a.split('>')
#         c = b[2].split('<')
#         listforbd.append(c[0])
#     return listforbd

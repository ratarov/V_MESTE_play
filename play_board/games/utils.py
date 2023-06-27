from .models import Game


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

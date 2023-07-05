import json
from pathlib import Path

from django.core.management.base import BaseCommand

from games.models import Game
from core.tesera_api import FIELDS


class Command(BaseCommand):
    help = 'Fills the DB with Games from json files'

    def parse_file(self, data_set):
        game_data = {}
        for field in FIELDS:
            game_data[FIELDS[field]] = data_set.get('game').get(field)
        return game_data

    def handle(self, *args, **kwargs):
        counter, new_games = 0, []
        for file in Path('static', 'json').iterdir():
            counter += 1
            self.stdout.write(f'{counter}. Открываем: {file}')
            with open(file, encoding='utf-8') as f:
                data = json.load(f)
                try:
                    game_dataset = self.parse_file(data)
                    new_games.append(Game(**game_dataset))
                except Exception:
                    self.stderr.write(
                        f"Не записана игра {game_dataset.get('alias')}.")
                    continue
        try:
            Game.objects.bulk_create(new_games, ignore_conflicts=True)
            self.stdout.write('Процесс успешно завершен\n'
                              f'Добавлено: {len(new_games)} / {counter}')
        except (ValueError,):
            self.stderr.write('Критическая ошибка - процесс остановлен.')

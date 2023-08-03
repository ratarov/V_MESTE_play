from random import randint

from django.utils import timezone
from django.core.management.base import BaseCommand

from matches.models import Player, Match


class Command(BaseCommand):
    help = 'Fills the DB with Games from json files'

    def handle(self, *args, **kwargs):
        for _ in range(1000):
            try:
                Match.objects.create(
                    date=timezone.now() - timezone.timedelta(days=randint(1,
                                                                          40)),
                    game_id=randint(1, 100),
                    place_id=randint(10, 40),
                    status=Match.Status.OK,
                )
            except Exception:
                pass

        for player_id in range(50, 84):
            for _ in range(50):
                try:
                    player = Player.objects.create(
                        match_id=randint(97, 1000),
                        name='Игрок',
                        user_id=player_id,
                        winner=randint(0, 1),
                    )
                    print('создал игрока', player.id)
                except Exception:
                    pass

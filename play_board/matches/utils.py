from django.db.transaction import atomic
from django.utils import timezone
from django.shortcuts import get_object_or_404

from meetings.models import Meeting

from .models import Match, Player


@atomic
def create_from_meeting(creator, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    args = {
        'creator': creator,
        'date': meeting.start_date,
        'game': meeting.games.all()[0],
        'place': meeting.place.get_name(),
    }
    participants = meeting.participants.all()
    users, guest_players = [], 0
    for part in participants:
        if part.status == 'ACT':
            guest_players += part.guests
            users.append(part.player)

    match = Match.objects.create(**args)

    players = []
    for user in users:
        players.append(
            Player(match=match, name=user.first_name, user=user)
        )
    for ind in range(1, guest_players + 1):
        players.append(
            Player(match=match, name=f'Игрок{ind}')
        )
    Player.objects.bulk_create(players)
    return match


@atomic
def create_from_match(creator, match_id):
    match = get_object_or_404(Match, id=match_id)
    old_players = list(match.players.select_related('user'))
    match.pk = None
    match.status = Match.Status.DRAFT
    match.creator = creator
    match.save()
    players = [Player(
        match=match, name=player.name, user=player.user, team=player.team
    ) for player in old_players]
    Player.objects.bulk_create(players)
    return match


@atomic
def create_new_match(creator):
    date = timezone.now().date()
    args = {
        'creator': creator,
        'date': date,
    }
    match = Match.objects.create(**args)
    Player.objects.create(
        match=match,
        name=creator.first_name,
        user=creator,
    )
    return match

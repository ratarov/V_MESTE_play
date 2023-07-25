from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Exists, OuterRef
from django.db.transaction import atomic
from django.shortcuts import get_object_or_404
from django.utils import timezone

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


def filter_user_matches(request):
    matches = (Match.objects.
               filter(players__user=request.user).
               annotate(is_winner=Exists(Player.objects.filter(
                   user=request.user, match_id=OuterRef('id'), winner=True
               ))).
               select_related('game', 'creator').
               prefetch_related('players', 'players__user'))
    status = request.GET.get('status')
    game = request.GET.get('game')
    date_since = request.GET.get('date_since')
    date_until = request.GET.get('date_until')
    if status:
        matches = matches.filter(status=status)
    if game:
        matches = matches.filter(game=game)
    if date_since:
        matches = matches.filter(date__gte=date_since)
    if date_until:
        matches = matches.filter(date__lte=date_until)
    return matches


def get_paginated_matches(queryset, request):
    """Пагинация списка матчей"""
    paginator = Paginator(queryset, settings.MATCHES_ON_PAGE)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)

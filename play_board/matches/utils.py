from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Exists, OuterRef, Q, Sum
from django.db.transaction import atomic
from django.shortcuts import get_object_or_404
from django.utils import timezone
from meetings.models import Meeting

from .models import Match, Player


def get_user_matches(user):
    return (Match.objects.
            filter(players__user=user).
            annotate(is_winner=Exists(Player.objects.filter(
                user=user, match_id=OuterRef('id'), winner=True
            ))).
            select_related('game', 'creator', 'place').
            prefetch_related('players', 'players__user'))


@atomic
def create_from_meeting(creator, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    args = {
        'creator': creator,
        'date': meeting.start_date,
        'game': meeting.games.all()[0],
        'place': meeting.place,
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
        username = user.username if user else ''
        players.append(
            Player(match=match, name=user.first_name,
                   user=user, username=username)
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
    match.date = timezone.now().date()
    match.save()
    players = [Player(
        match=match, name=player.name, user=player.user,
        team=player.team, username=player.username,
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
        username=creator.username,
    )
    return match


def filter_user_matches(request):
    matches = get_user_matches(request.user)
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


def filter_match_plays(request, match_plays):
    game = request.GET.get('game')
    date_since = request.GET.get(
        'date_since', default=timezone.now() - timezone.timedelta(days=90)
    )
    date_until = request.GET.get('date_until', default=timezone.now())
    place = request.GET.get('place')
    type = request.GET.get('type')
    player = request.GET.get('player')

    match_plays = match_plays.filter(match__date__gte=date_since,
                                     match__date__lte=date_until)
    if game:
        match_plays = match_plays.filter(match__game=game)
    if place:
        match_plays = match_plays.filter(match__place=place)
    if type:
        match_plays = match_plays.filter(match__type=type)
    if player:
        return match_plays.filter(Q(user=player) | Q(user=request.user))
    return match_plays


def get_common_stats(match_plays, user):
    return (match_plays.filter(user=user).aggregate(
        total=Sum('match__quantity'),
        wins=Sum('match__quantity', filter=Q(winner=True)),
        avg_length=Avg('match__length', filter=Q(match__length__gte=0)),
        games=Count('match__game', distinct=True),
    ))


def get_games_stat(match_plays, user):
    return (match_plays.
            filter(user=user).
            values('match__game__name_rus').
            annotate(
                total=Sum('match__quantity'),
                losts=Sum('match__quantity', filter=Q(winner=False)),
                wins=Sum('match__quantity', filter=Q(winner=True)),
            ).
            order_by('-total'))


def get_player_stats(match_plays):
    return (match_plays.
            exclude(user=None).values('user__username').
            annotate(
                total=Sum('match__quantity'),
                wins=Sum('match__quantity', filter=Q(winner=True)),
                losts=Sum('match__quantity', filter=Q(winner=False)),
                games=Count('match__game', distinct=True),
            ).
            order_by('-total'))


def get_places_stats(match_plays, user):
    return (match_plays.
            filter(user=user).values('match__place__name').
            annotate(total=Sum('match__quantity')).
            order_by('-total'))

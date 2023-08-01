from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from games.models import Game
from users.models import User

from .forms import MatchForm, PlayerForm, UserMatchesForm, StatFilterForm
from .models import Match, Player
from .utils import (create_from_match, create_from_meeting, create_new_match,
                    filter_user_matches, get_paginated_matches,
                    get_user_matches)


@login_required
def my_matches(request):
    """Список партий пользователя."""
    form = UserMatchesForm(data=request.GET or None)
    matches = filter_user_matches(request)
    matches = get_paginated_matches(matches, request)
    context = {'matches': matches, 'form': form}
    if request.GET.get('page'):
        return render(request, 'matches/match_items.html', context)
    return render(request, 'matches/my_matches.html', context)


def match_detail(request, match_id):
    """Страница с деталями о конкретной партии"""
    match = get_object_or_404(
        (Match.objects.
         select_related('creator', 'game').
         prefetch_related('players', 'players__user')
         ),
        pk=match_id,
    )
    is_player = False
    if request.user.is_authenticated:
        is_player = match.players.filter(user=request.user)
    context = {'match': match, 'is_player': is_player}
    return render(request, 'matches/match_detail.html', context)


@login_required
def match_create_from_meeting(request, meeting_id):
    """Создание новой партии на основании встречи."""
    match = create_from_meeting(request.user, meeting_id)
    return redirect('matches:match_edit', match.id)


@login_required
def match_create_from_match(request, match_id):
    """Создание новой партии на основании другой партии."""
    match = create_from_match(request.user, match_id)
    return redirect('matches:match_edit', match.id)


@login_required
def match_create_new(request):
    """Создание новой пустой партии."""
    match = create_new_match(request.user)
    return redirect('matches:match_edit', match.id)


@login_required
def match_edit(request, match_id):
    """Корректировка партии."""
    match = get_object_or_404(
        (Match.objects.
         select_related('creator').
         prefetch_related('players', 'players__user', 'players__user__places')
         ),
        pk=match_id,
    )
    if match.creator != request.user:
        return redirect('matches:match_detail', pk=match_id)
    match_form = MatchForm(request.POST or None, instance=match)
    player_form = PlayerForm(request.POST or None)
    if request.method == 'POST':
        if match_form.is_valid():
            match = match_form.save()
            return redirect('matches:match_detail', match_id)
        if player_form.is_valid():
            player = player_form.save(commit=False)
            player.match = match
            player.save()
            return redirect('matches:player_detail', player.id)
        else:
            context = {'player_form': player_form}
            return render(request, 'matches/player_form.html', context)

    context = {
        'player_form': player_form,
        'match_form': match_form,
        'match': match,
    }
    return render(request, 'matches/match_edit.html', context)


@login_required
def match_delete(request, match_id):
    """Удаление париии"""
    match = get_object_or_404(Match.objects.select_related('creator'),
                              pk=match_id)
    if match.creator != request.user:
        return redirect('matches:match_detail', match_id)
    match.delete()
    if 'htmx' in request.path:
        return HttpResponse('')
    return redirect('matches:my_matches')


@login_required
def match_leave(request, match_id):
    """Покинуть партию - удалить связь юзера с игроком в партии."""
    player = Player.objects.filter(user=request.user,
                                   match_id=match_id).first()
    if player:
        player.user = None
        player.save()
    return redirect('matches:match_detail', match_id)


@login_required
def create_player_form(request):
    """Создание новой строки игрока в партии."""
    context = {'player_form': PlayerForm, 'users': User.objects.all()}
    return render(request, 'matches/player_form.html', context)


@login_required
def player_detail(request, player_id):
    """Строка с информацией об игроке в партии."""
    player = get_object_or_404(Player, pk=player_id)
    context = {'player': player}
    return render(request, 'matches/player_detail.html', context)


@login_required
def player_edit(request, player_id):
    """Изменение строки с данными игрока в партии"""
    player = get_object_or_404(Player, pk=player_id)
    player_form = PlayerForm(request.POST or None, instance=player)
    if player_form.is_valid():
        player = player_form.save()
        return redirect('matches:player_detail', player.id)

    context = {
        'player_form': player_form,
        'player': player,
        'users': User.objects.all(),
    }
    return render(request, 'matches/player_form.html', context)


@login_required
def player_delete(request, player_id):
    """Удаление строки с игроком из партии."""
    player = get_object_or_404(Player, pk=player_id)
    player.delete()
    return HttpResponse('')

from django.db.models import Sum, Count, Q, Avg, Func
from django.utils import timezone
from datetime import datetime
from django.db import connection

@login_required
def statistics(request):
    """Список партий пользователя."""
    match_plays = Player.objects.filter(match__players__user=request.user, match__status=Match.Status.OK).select_related('user', 'match', 'match__game')
    common_stat = match_plays.filter(user=request.user).aggregate(
        total=Sum('match__quantity'),
        wins=Sum('match__quantity', filter=Q(winner=True)),
        avg_length=Avg('match__length', filter=Q(match__length__gte=0)),
        games=Count('match__game', distinct=True),
        # one=Sum('match__quantity', filter=Count('meeting__players')=1),
        # two=Sum('match__quantity', filter=Q(Count('meeting__players')==2)),
        three=Sum('match__quantity', filter=Q(Count('match__players')==3)),
        # four=Sum('match__quantity', filter=Q(pl_qty=4)),
        # five=Sum('match__quantity', filter=Q(pl_qty=5)),
        # six=Sum('match__quantity', filter=Q(pl_qty__gte=6)),
    )
    print('а вот и ',common_stat.get('three'))
    games = match_plays.filter(user=request.user)
    games = games.values(
        'match__game__name_rus',
    ).annotate(
        total=Sum('match__quantity'),
        losts=Sum('match__quantity', filter=Q(winner=False)),
        wins=Sum('match__quantity', filter=Q(winner=True)),
    ).order_by('-total')

    players = match_plays.exclude(user=None).values(
        'user__username',
    ).annotate(
        total=Sum('match__quantity'),
        wins=Sum('match__quantity', filter=Q(winner=True)),
        losts=Sum('match__quantity', filter=Q(winner=False)),
        games=Count('match__game'),
    ).order_by('-total')

    places = match_plays.filter(user=request.user).values(
        'match__place'
    ).annotate(
        total=Sum('match__quantity'),
        games=Count('match__game'),
    ).order_by('-total')

    form = StatFilterForm(places=places, players=players, games=games, data=request.GET or None)
    context = {
        'matches': common_stat,
        'players': players,
        'games': games,
        'places': places,
        'form': form,
    }
    return render(request, 'matches/stats.html', context)

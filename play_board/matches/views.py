from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from users.models import User

from .forms import MatchForm, PlayerForm, StatFilterForm, UserMatchesForm
from .models import Match, Player
from .utils import (create_from_match, create_from_meeting, create_new_match,
                    filter_match_plays, filter_user_matches, get_common_stats,
                    get_games_stat, get_paginated_matches, get_places_stats,
                    get_player_stats)


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
        return redirect('matches:match_detail', match_id)
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


@login_required
def statistics(request):
    """Статистика партий пользователя."""
    user = request.user
    match_plays = Player.objects.filter(match__players__user=user,
                                        match__status=Match.Status.OK)

    form = StatFilterForm(user=user, data=request.GET or None)
    match_plays = filter_match_plays(request, match_plays)

    common_stat = get_common_stats(match_plays, user)
    games = get_games_stat(match_plays, user)
    players = get_player_stats(match_plays)
    places = get_places_stats(match_plays, user)

    context = {
        'matches': common_stat,
        'players': players,
        'games': games,
        'places': places,
        'form': form,
    }
    return render(request, 'matches/stats.html', context)

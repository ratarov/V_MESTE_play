from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from games.models import Game
from games.utils import (parse_tesera_response, search_games,
                         update_game_data)
from django.contrib.auth.decorators import login_required


def game_detail(request, game_slug):
    """Страница игры со всеми деталями"""
    game = get_object_or_404(Game, slug=game_slug)
    if not any([game.bgg_id, game.description]):
        update_game_data(game)
    liked = (request.user.is_authenticated and
             request.user.liked_games.filter(slug=game_slug).exists())
    collected = (request.user.is_authenticated and
                 request.user.site_collection.filter(slug=game_slug).exists())
    context = {'game': game, 'liked': liked, 'collected': collected}
    return render(request, 'games/game_detail.html', context)


def game_add(request):
    """Страница поиска и добавления игры из базы на tesera.ru"""
    search = request.GET.get('search')
    context = {'new_search': True}
    if search:
        new_games = []
        games_in_base = list(Game.objects.values_list('slug', flat=True))
        search_result = search_games(search)
        if search_result:
            games_data = parse_tesera_response(search_result)
            print(f'геймз дата: {games_data}')
            for game_dataset in games_data:
                if game_dataset.get('slug') not in games_in_base:
                    new_games.append(Game(**game_dataset))
            print(new_games)
            Game.objects.bulk_create(new_games)
        context['search'] = True
        context['games'] = new_games
    return render(request, 'games/game_search.html', context)


def game_search(request):
    """Страница поиска игры в существующей базе сайта"""
    search = request.GET.get('search')
    context = {'existing_search': True}
    if search:
        games = Game.objects.filter(
            Q(name_rus__icontains=search) | Q(name_eng__icontains=search))
        context['search'] = True
        context['games'] = games
    return render(request, 'games/game_search.html', context)


@login_required
def like_game(request, game_slug):
    """Добавление/удаление лайка игре (список любимых игр пользователя)"""
    game = get_object_or_404(Game, slug=game_slug)
    if request.user.liked_games.filter(slug=game_slug).exists():
        request.user.liked_games.remove(game)
    else:
        request.user.liked_games.add(game)
    return redirect('games:game_detail', game_slug)


@login_required
def collect_game(request, game_slug):
    """Добавление/удаление игры в коллекцию пользователя на сайте"""
    game = get_object_or_404(Game, slug=game_slug)
    if request.user.site_collection.filter(slug=game_slug).exists():
        request.user.site_collection.remove(game)
    else:
        request.user.site_collection.add(game)
    return redirect('games:game_detail', game_slug)

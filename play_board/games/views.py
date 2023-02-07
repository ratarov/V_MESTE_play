from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from games.models import Game
from games.utils import (create_game, parse_tesera_response, search_games,
                         update_game_data)
from django.contrib.auth.decorators import login_required


def game_detail(request, game_slug):
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
    search = request.GET.get('search')
    context = {'new_search': True}
    if search:
        new_games_data = []
        games_in_base = list(Game.objects.values_list('slug', flat=True))
        search_result = search_games(search)
        if search_result:
            games_data = parse_tesera_response(search_result)
            for game_dataset in games_data:
                if game_dataset.get('slug') not in games_in_base:
                    new_games_data.append(game_dataset)
                    create_game(game_dataset)
        context['search'] = True
        context['games'] = new_games_data
    return render(request, 'games/game_search.html', context)


def game_search(request):
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
    game = get_object_or_404(Game, slug=game_slug)
    if request.user.liked_games.filter(slug=game_slug).exists():
        request.user.liked_games.remove(game)
    else:
        request.user.liked_games.add(game)
    return redirect('games:game_detail', game_slug)

    
@login_required
def collect_game(request, game_slug):
    game = get_object_or_404(Game, slug=game_slug)
    if request.user.site_collection.filter(slug=game_slug).exists():
        request.user.site_collection.remove(game)
    else:
        request.user.site_collection.add(game)
    return redirect('games:game_detail', game_slug)
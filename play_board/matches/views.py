from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from users.models import User

from .forms import PlayerForm, MatchForm
from .models import Match, Player
from .utils import create_from_meeting, create_from_match, create_new_match


@login_required
def my_matches(request):
    matches = Match.objects.filter(players__user=request.user)
    context = {'matches': matches}
    return render(request, 'matches/my_matches.html', context)


def match_detail(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    context = {'match': match}
    return render(request, 'matches/match_detail.html', context)


@login_required
def match_create_from_meeting(request, meeting_id):
    match = create_from_meeting(request.user, meeting_id)
    return redirect('matches:match_edit', match.id)


@login_required
def match_create_from_match(request, match_id):
    match = create_from_match(request.user, match_id)
    return redirect('matches:match_edit', match.id)


@login_required
def match_create_new(request):
    match = create_new_match(request.user)
    return redirect('matches:match_edit', match.id)


@login_required
def match_edit(request, match_id):
    match = get_object_or_404(Match.objects.select_related('creator'),
                              pk=match_id)
    if match.creator != request.user:
        return redirect('matches:match_detail', pk=match_id)
    match_form = MatchForm(request.POST or None, instance=match)
    player_form = PlayerForm(request.POST or None)
    if request.method == 'POST':
        if match_form.is_valid():
            match = match_form.save()
            return redirect('matches:my_matches')
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
    match = get_object_or_404(Match.objects.select_related('creator'),
                              pk=match_id)
    if match.creator != request.user:
        return redirect('matches:match_detail', pk=match_id)
    match.delete()
    return redirect('matches:my_matches')


@login_required
def create_player_form(request):
    context = {'player_form': PlayerForm, 'users': User.objects.all()}
    return render(request, 'matches/player_form.html', context)


@login_required
def player_detail(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    context = {'player': player}
    return render(request, 'matches/player_detail.html', context)


@login_required
def player_edit(request, player_id):
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
    player = get_object_or_404(Player, pk=player_id)
    player.delete()
    return HttpResponse('')

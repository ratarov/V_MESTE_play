from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from games.models import Game
from users.forms import (CreateUserForm, PlaceForm, UserInfoForm,
                         UserMeetingsForm)
from users.models import Place, User
from users.utils import (get_tesera_collection, get_tesera_user,
                         get_paginated_games, filter_user_meetings)
from games.utils import parse_tesera_response


def gamer_profile(request, username):
    gamer = get_object_or_404(User, username=username)
    context = {'gamer': gamer}
    return render(request, 'users/gamer_profile.html', context)


def gamer_collections(request, username, collection):
    gamer = get_object_or_404(User, username=username)
    qs = {
        'liked': gamer.liked_games.all(),
        'site': gamer.site_collection.all(),
        'tesera': gamer.tesera_collection.all(),
    }
    games = get_paginated_games(qs[collection], request)
    context = {'page_obj': games, 'type': collection, 'user': gamer}
    return render(request, 'users/user_collections.html', context)


@login_required
def user_info(request):
    return render(request, 'users/user_info.html')


@login_required
def user_info_edit(request):
    places = Place.objects.filter(creator=request.user).select_related('type')
    form = UserInfoForm(request.POST or None, files=request.FILES or None,
                        instance=request.user)
    if form.is_valid():
        user = form.save(commit=False)
        user.save()
        return redirect('users:user_info')
    context = {'form': form, 'places': places}
    return render(request, 'users/user_info_edit.html', context)


@login_required
def update_tesera_collection(request):
    if request.user.tesera_account:
        collection_qty = get_tesera_user(request.user.tesera_account)
        if collection_qty:
            collection_raw = get_tesera_collection(
                request.user.tesera_account, collection_qty)
            collection_dataset = parse_tesera_response(collection_raw)
            request.user.tesera_collection.clear()
            new_games = []
            games_in_collection = []
            games_in_base = list(Game.objects.values_list('slug', flat=True))
            for game_dataset in collection_dataset:
                slug = game_dataset.get('slug')
                if slug not in games_in_base:
                    new_games.append(Game(**game_dataset))
                games_in_collection.append(slug)
            Game.objects.bulk_create(new_games)
            games_in_base = dict(Game.objects.values_list('slug', 'id'))
            mapped_games = map(lambda x: games_in_base.get(x),
                               games_in_collection)
            col = [User.tesera_collection.through(
                user_id=request.user.id, game_id=xxx) for xxx in mapped_games]
            User.tesera_collection.through.objects.bulk_create(col)
    return redirect('users:user_collections', 'tesera')


@login_required
def user_collections(request, collection):
    qs = {
        'liked': request.user.liked_games.all(),
        'site': request.user.site_collection.all(),
        'tesera': request.user.tesera_collection.all(),
    }
    games = get_paginated_games(qs[collection], request)
    context = {'page_obj': games, 'type': collection}
    return render(request, 'users/user_collections.html', context)


@login_required
def user_meetings(request):
    form = UserMeetingsForm(data=request.GET or None)
    meetings = filter_user_meetings(request)
    context = {'meetings': meetings, 'form': form}
    return render(request, 'users/user_meetings.html', context)


@login_required
def place_add(request):
    form = PlaceForm(request.POST or None)
    if form.is_valid():
        place = form.save(commit=False)
        place.creator = request.user
        place.save()
        return redirect('users:user_info')
    context = {'form': form}
    return render(request, 'users/place_add_or_edit.html', context)


@login_required
def place_edit(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    if request.user != place.creator:
        return redirect('users:user_info')
    form = PlaceForm(request.POST or None, instance=place)
    if form.is_valid():
        place = form.save(commit=False)
        place.save()
        return redirect('users:user_info')
    context = {
        'form': form,
        'is_edit': True
    }
    return render(request, 'users/place_add_or_edit.html', context)


@login_required
def place_del(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    if request.user == place.creator:
        place.delete()
    return redirect('users:user_info')


# Registration activity

class SignUp(CreateView):
    form_class = CreateUserForm
    success_url = reverse_lazy('meetings:index')
    template_name = 'users/reg_actions/signup.html'


class MyPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/reg_actions/password_change_form.html'

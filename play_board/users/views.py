from math import cos, pi

import folium
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from core.geolocation import get_geolocation
from core.tesera_api import parse_tesera_response, get_tesera_collection
from core.exceptions import EndpointError
from games.models import Game

from .forms import (CreateUserForm, PlaceForm, UserInfoForm,
                    UserMeetingsForm, BotConfigForm)
from .models import Place, User, BotConfig
from .utils import (get_paginated_games, filter_user_meetings,
                    add_search_marker)


def gamer_profile(request, username):
    """Страница пользователя - доступна всем"""
    gamer = get_object_or_404(User, username=username)
    cancelled = gamer.created.filter(status=3).count()
    joined = gamer.participated.exclude(meeting__creator=gamer).count()
    context = {'gamer': gamer, 'cancelled': cancelled, 'joined': joined}
    return render(request, 'users/gamer_profile.html', context)


def gamer_collections(request, username, collection):
    """
    Страница со списком игр в выбранной коллекции:
    любимые, коллекция на сайте и коллекция на tesera.ru
    """
    gamer = get_object_or_404(User, username=username)
    qs = {
        'liked': gamer.liked_games.all(),
        'site': gamer.site_collection.all(),
        'tesera': gamer.tesera_collection.all(),
    }
    if collection not in qs:
        return redirect('users:profile', username)
    games = get_paginated_games(qs.get(collection), request)
    context = {'page_obj': games, 'type': collection, 'user': gamer}
    return render(request, 'users/user_collections.html', context)


@login_required
def user_info(request):
    """Личный кабинет пользователя"""
    return render(request, 'users/user_info.html')


@login_required
def user_info_edit(request):
    """Страница изменения личных данных пользователя"""
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
    """Функция обновления списка игр в коллекции на сайте tesera.ru"""
    if request.user.tesera_account:
        collection_raw = get_tesera_collection(request.user.tesera_account)
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
    return redirect('users:user_info')


@login_required
def user_collections(request, collection):
    """Страница со списком игр в коллекции пользователя"""
    qs = {
        'liked': request.user.liked_games.all(),
        'site': request.user.site_collection.all(),
        'tesera': request.user.tesera_collection.all(),
    }
    if collection not in qs:
        return redirect('users:user_info')
    games = get_paginated_games(qs.get(collection), request)
    context = {'page_obj': games, 'type': collection}
    return render(request, 'users/user_collections.html', context)


@login_required
def user_bot_config(request):
    """Страница с настройками телеграм-бота"""
    bot_config = get_object_or_404(BotConfig, user=request.user)
    form = BotConfigForm(request.POST or None, instance=bot_config)
    if form.is_valid():
        bot_config = form.save(commit=False)
        if form.data.get('new_meeting_info'):
            try:
                geolocation = get_geolocation(form.data.get('address'))
            except EndpointError:
                
                return redirect('users:user_bot_config')
            if geolocation:
                lat_diff = int(form.data.get('radius')) / settings.KM_IN_DEGREE
                lon_diff = int(form.data.get('radius')) / (cos(
                    float(geolocation.latitude) / 180 * pi
                ) * settings.KM_IN_DEGREE)
                bot_config.loc_lat = geolocation.latitude
                bot_config.loc_lon = geolocation.longitude
                bot_config.min_lat = bot_config.loc_lat - lat_diff
                bot_config.max_lat = bot_config.loc_lat + lat_diff
                bot_config.min_lon = bot_config.loc_lon - lon_diff
                bot_config.max_lon = bot_config.loc_lon + lon_diff
        bot_config.save()
        bot_config.games.clear()
        bot_config.games.set(form.data.getlist('games'))
        return redirect('users:user_bot_config')
    context = {'form': form}
    if bot_config.new_meeting_info and bot_config.loc_lat:
        start = [bot_config.loc_lat, bot_config.loc_lon]
        map = folium.Map(
            location=start,
            zoom_start=13,
        )
        add_search_marker(map, bot_config)
        map = map._repr_html_()
        context['map'] = map
    return render(request, 'users/user_bot_config.html', context)


@login_required
def user_meetings(request):
    """Страница со спиком встреч пользователя"""
    form = UserMeetingsForm(data=request.GET or None)
    meetings = filter_user_meetings(request)
    context = {'meetings': meetings, 'form': form}
    return render(request, 'users/user_meetings.html', context)


@login_required
def place_add(request):
    """Страница добавления новых мест пользователя для встреч"""
    form = PlaceForm(request.POST or None)
    if form.is_valid():
        place = form.save(commit=False)
        place.creator = request.user
        place.loc_lat = form.cleaned_data.get('loc_lat')
        place.loc_lon = form.cleaned_data.get('loc_lon')
        place.save()
        return redirect('users:user_info')
    context = {'form': form}
    return render(request, 'users/place_add_or_edit.html', context)


@login_required
def place_edit(request, place_id):
    """Страница изменения существующего места пользователя для встреч"""
    place = get_object_or_404(Place, id=place_id)
    if request.user != place.creator:
        return redirect('users:user_info')
    form = PlaceForm(request.POST or None, instance=place)
    if form.is_valid():
        place = form.save(commit=False)
        place.loc_lat = form.cleaned_data.get('loc_lat')
        place.loc_lon = form.cleaned_data.get('loc_lon')
        place.save()
        return redirect('users:user_info')
    context = {
        'form': form,
        'is_edit': True
    }
    return render(request, 'users/place_add_or_edit.html', context)


@login_required
def place_del(request, place_id):
    """Функция удаления места пользователя для встреч"""
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

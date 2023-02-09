import folium
from folium.plugins import MarkerCluster
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from meetings.forms import (CommentForm, MeetingForm, MeetingSearchForm,
                            GuestForm)
from meetings.models import (Comment, Meeting, MeetingStatus,
                             MeetingParticipation)
from users.models import User
from meetings.utils import get_geolocation, filter_meetings, add_meeting_marker
from django.conf import settings


def index(request):
    form = MeetingSearchForm()
    context = {'form': form}
    return render(request, 'meetings/index.html', context)


def meeting_search(request):
    form = MeetingSearchForm(data=request.GET or None)
    location = request.GET.get('location')
    context = {'form': form, }

    if location:
        text = f'Место "{location}" не найдено на карте'
        geolocation = get_geolocation(location)
        if geolocation:
            radius = request.GET.get('radius', settings.DEFAULT_SEARCH_RADIUS)
            meetings = filter_meetings(geolocation, request)
            text = (f'В радиусе {radius} км от "{location}" найдено '
                    f'встреч: {len(meetings)}')

            start = [geolocation.latitude, geolocation.longitude]
            map = folium.Map(
                location=start,
                zoom_start=11,
            )
            cluster_map = MarkerCluster(name='Встречи').add_to(map)
            for meeting in meetings:
                add_meeting_marker(cluster_map, meeting)
            folium.LayerControl().add_to(map)
            map = map._repr_html_()
            context['meetings'] = meetings
            context['map'] = map
        context['text'] = text
    return render(request, 'meetings/meeting_search.html', context)


@login_required
def meeting_create(request):
    meeting_form = MeetingForm(user=request.user, data=request.POST or None)
    if meeting_form.is_valid():
        meeting = meeting_form.save(commit=False)
        meeting.creator = request.user
        meeting.status = MeetingStatus.objects.get(name='Готовится')
        meeting.save()
        meeting.participants.create(
            player=request.user,
            guests=meeting_form.data.get('guests')
        )
        for game in meeting_form.data.getlist('games'):
            meeting.games.add(game)
        return redirect('meetings:meeting_detail', meeting.pk)
    context = {
        'meeting_form': meeting_form,
    }
    return render(request, 'meetings/meeting_create.html', context)


def meeting_detail(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    comments = meeting.comments.select_related('creator')
    comment_form = CommentForm()

    participation = None
    if request.user.is_authenticated and meeting.participants.\
            filter(player=request.user).exists():
        participation = meeting.participants.get(player=request.user)

    guests_form = GuestForm(user=request.user, meeting=meeting,
                            data=request.POST or None, instance=participation)

    if guests_form.is_valid():
        return redirect('meetings:join_meeting',
                        guests=guests_form.data.get('guests'),
                        meeting_id=meeting_id)

    start = [meeting.place.loc_lat, meeting.place.loc_lon]
    map = folium.Map(
        location=start,
        zoom_start=13,
    )
    add_meeting_marker(map, meeting)
    map = map._repr_html_()
    context = {
        'meeting': meeting,
        'comments': comments,
        'comment_form': comment_form,
        'guests_form': guests_form,
        'map': map,
        'participation': participation,
    }
    return render(request, 'meetings/meeting_detail.html', context)


@login_required
def meeting_edit(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    if meeting.creator != request.user:
        return redirect('meetings:meeting_detail', meeting.id)

    meeting_form = MeetingForm(user=request.user, data=request.POST or None,
                               instance=meeting)
    participation = meeting.participants.get(player=request.user)
    if meeting_form.is_valid():
        meeting = meeting_form.save(commit=False)
        meeting.save()
        meeting.games.clear()
        for game in meeting_form.data.getlist('games'):
            meeting.games.add(game)
        participation.guests = meeting_form.data.get('guests')
        participation.save()
        return redirect('meetings:meeting_detail', meeting.id)
    context = {
        'meeting_form': meeting_form,
        'form_edit': True
    }
    return render(request, 'meetings/meeting_create.html', context)


@login_required
def meeting_cancel(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    if request.user == meeting.creator:
        meeting.status = MeetingStatus.objects.get(name='Отменена')
        meeting.save()
    return redirect('meetings:meeting_detail', meeting_id)


@login_required
def join_meeting(request, guests, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    if not meeting.participants.filter(player=request.user).exists():
        meeting.participants.create(
            player=request.user,
            guests=guests
        )
    else:
        participation = meeting.participants.get(player=request.user)
        participation.guests = guests
        participation.save()
    return redirect('meetings:meeting_detail', meeting_id)


@login_required
def leave_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    participation = get_object_or_404(MeetingParticipation, meeting=meeting,
                                      player=request.user)
    if request.user != meeting.creator:
        participation.delete()
    return redirect('meetings:meeting_detail', meeting_id)


@login_required
def ban_player(request, meeting_id, username):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    player = get_object_or_404(User, username=username)
    participation = get_object_or_404(MeetingParticipation, meeting=meeting,
                                      player=player)
    if meeting.creator == request.user and meeting.creator != player:
        participation.status = 'BAN'
        participation.save()
    return redirect('meetings:meeting_detail', meeting_id)


@login_required
def unban_player(request, meeting_id, username):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    player = get_object_or_404(User, username=username)
    participation = get_object_or_404(MeetingParticipation, meeting=meeting,
                                      player=player)
    if meeting.creator == request.user:
        if (participation.guests + 1 + meeting.get_total_players())\
                <= meeting.max_players:
            participation.status = 'ACT'
            participation.save()
        else:
            participation.delete()
    return redirect('meetings:meeting_detail', meeting_id)


@login_required
def comment_add(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.creator = request.user
        comment.meeting = meeting
        comment.save()
    return redirect('meetings:meeting_detail', meeting_id)


@login_required
def comment_del(request, meeting_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.creator == request.user:
        comment.delete()
    return redirect('meetings:meeting_detail', meeting_id)

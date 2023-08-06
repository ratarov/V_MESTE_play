from django.urls import path

from . import views

app_name = 'matches'

urlpatterns = [
    path('htmx/player-form/',
         views.create_player_form, name='player_form'),
    path('htmx/player/<int:player_id>/delete/',
         views.player_delete, name='player_delete'),
    path('htmx/player/<int:player_id>/edit/',
         views.player_edit, name='player_edit'),
    path('htmx/player/<int:player_id>/',
         views.player_detail, name='player_detail'),
    path('htmx/<int:match_id>/delete/',
         views.match_delete, name='match_delete_from_list'),
    path('<int:match_id>/edit/',
         views.match_edit, name='match_edit'),
    path('<int:match_id>/delete/',
         views.match_delete, name='match_delete'),
    path('<int:match_id>/leave/',
         views.match_leave, name='match_leave'),
    path('<int:match_id>/',
         views.match_detail, name='match_detail'),
    path('create-from-meeting-<int:meeting_id>/',
         views.match_create_from_meeting, name='create_from_meeting'),
    path('create-from-match-<int:match_id>/',
         views.match_create_from_match, name='create_from_match'),
    path('create-new/',
         views.match_create_new, name='create_new_match'),
    path('stats/',
         views.statistics, name='stats'),
    path('', views.my_matches, name='my_matches'),
]

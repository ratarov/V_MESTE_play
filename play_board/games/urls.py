from django.urls import path

from . import views


app_name = 'games'

urlpatterns = [
    path('add/', views.game_add, name='game_add'),
    path('<slug:game_slug>/like', views.like_game, name='like_game'),
    path('<slug:game_slug>/collect', views.collect_game, name='collect_game'),
    path('<slug:game_slug>/', views.game_detail, name='game_detail'),
    path('', views.game_search, name='game_search'),
]

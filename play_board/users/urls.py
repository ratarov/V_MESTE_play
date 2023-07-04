from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeDoneView,
                                       PasswordResetView)
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('my-info/edit/', views.user_info_edit, name='user_info_edit'),
    path('my-info/', views.user_info, name='user_info'),
    path('my-collections/<str:collection>/', views.user_collections,
         name='user_collections'),
    path('my-collections/update/', views.update_tesera_collection,
         name='update_collection'),
    path('my-meetings/', views.user_meetings, name='user_meetings'),
    path('my-bot-settings/', views.user_bot_config, name='user_bot_config'),
    path('places/add/', views.place_add, name='place_add'),
    path('places/<int:place_id>/edit/', views.place_edit, name='place_edit'),
    path('places/<int:place_id>/del/', views.place_del, name='place_del'),
    path('profile/<str:username>/', views.gamer_profile, name='profile'),
    path('profile/<str:username>/<str:collection>/', views.gamer_collections,
         name='gamer_collections'),

    # registration & authentication actions
    path('signup/',
         views.SignUp.as_view(template_name='users/reg_actions/signup.html'),
         name='signup'),
    path('login/',
         LoginView.as_view(template_name='users/reg_actions/login.html'),
         name='login'),
    path('login2/',
         LoginView.as_view(template_name='users/reg_actions/login2.html'),
         name='login2'),
    path('logout/',
         LogoutView.as_view(
             template_name='users/reg_actions/logged_out.html'),
         name='logout'),
    path('password_change/done/',
         PasswordChangeDoneView.as_view(
             template_name='users/reg_actions/password_change_done.html'),
         name='password_change_done'),
    path('password_change/',
         views.MyPasswordChangeView.as_view(
             template_name='users/reg_actions/password_change_form.html'),
         name='password_change'),
    path('password_reset/',
         PasswordResetView.as_view(
             template_name='users/reg_actions/password_reset_form.html'),
         name='password_reset'),
]

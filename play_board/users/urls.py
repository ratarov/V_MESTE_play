from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeDoneView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
     path('my-info/edit', views.user_info_edit, name='user_info_edit'),
     path('my-info/', views.user_info, name='user_info'),
     path('my-info/<str:collection>/', views.user_collections,
          name='user_collections'),
     path('my-collections/update', views.update_tesera_collection,
          name='update_collection'),
     path('my-meetings/', views.user_meetings, name='user_meetings'),
     path('places/add/', views.place_add, name='place_add'),
     path('places/<int:place_id>/edit/', views.place_edit, name='place_edit'),
     path('places/<int:place_id>/del/', views.place_del, name='place_del'),
     path('profile-<slug:username>/', views.gamer_profile, name='profile'),
     path('profile-<slug:username>/<str:collection>', views.gamer_collections,
          name='gamer_collections'),
     # registration_actions
     path('signup/',
          views.SignUp.as_view(template_name='users/reg_actions/signup.html'),
          name='signup'),
     path('login/',
          LoginView.as_view(template_name='users/reg_actions/login.html'),
          name='login'),
     path('logout/', LogoutView.as_view(
                    template_name='users/reg_actions/logged_out.html'
               ), name='logout'),
     path('password_change/done/', PasswordChangeDoneView.as_view(
                    template_name='users/reg_actions/password_change_done.html'
               ), name='password_change_done'),
     path('password_change/', views.MyPasswordChangeView.as_view(
                    template_name='users/reg_actions/password_change_form.html'
               ), name='password_change'),
]

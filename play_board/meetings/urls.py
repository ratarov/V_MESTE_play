from django.urls import path

from . import views


app_name = 'meetings'

urlpatterns = [

     path('meetings/create/', views.meeting_create, name='meeting_create'),
     path('meetings/<int:meeting_id>/edit/', views.meeting_edit,
          name='meeting_edit'),
     path('meetings/<int:meeting_id>/cancel/', views.meeting_cancel,
          name='meeting_cancel'),
     path('meetings/<int:meeting_id>/', views.meeting_detail,
          name='meeting_detail'),
     path('meetings/<int:meeting_id>/join+<int:guests>/',
          views.join_meeting, name='join_meeting'),
     path('meetings/<int:meeting_id>/leave/',
          views.leave_meeting, name='leave_meeting'),
     path('meetings/<int:meeting_id>/ban/<str:username>/',
          views.ban_player, name='ban_player'),
     path('meetings/<int:meeting_id>/unban/<str:username>/',
          views.unban_player, name='unban_player'),
     path('meetings/<int:meeting_id>/comments/add/', views.comment_add,
          name='comment_add'),
     path('meetings/<int:meeting_id>/comments/<int:comment_id>/del/',
          views.comment_del, name='comment_del'),
     path('meetings/', views.meeting_search, name='meeting_search'),
     path('', views.index, name='index'),
]

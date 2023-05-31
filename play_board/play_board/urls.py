from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import (PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView)
from django.urls import include, path


urlpatterns = [
    path('adminka/', admin.site.urls),
    path('games/', include('games.urls', namespace='games')),
    path('users/', include('users.urls', namespace='users')),

    path('users/reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name='users/reg_actions/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('users/password_reset/done/',
         PasswordResetDoneView.as_view(
             template_name='users/reg_actions/password_reset_done.html'),
         name='password_reset_done'),
    path('users/reset/done/',
         PasswordResetCompleteView.as_view(
             template_name='users/reg_actions/password_reset_complete.html'),
         name='password_reset_complete'),

    path('', include('meetings.urls', namespace='meetings')),
]

handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'
handler403 = 'core.views.permission_denied'

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),

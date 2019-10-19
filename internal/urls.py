from django.urls import path, re_path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
# from django.shortcuts import redirect
from django.views.generic.base import RedirectView
from challenge import urls

from . import views

urlpatterns = [
    path('', views.index_view, name='index'),

    # auth / admin
    path('register/', views.register_view, name='bitbyte_register'),
    path('register/submit/', views.register_submit_view, name='bitbyte_register_submit'),
    path('login/', views.login_view, name='bitbyte_login'),
    path('login/submit/', views.login_submit_view, name='bitbyte_login_submit'),
    path('logout/', views.logout_view, name='bitbyte_logout'),
    path('editprofile/', views.edit_profile_view, name='bitbyte_edit_profile'),

    # builtin auth
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="internal/password_reset.html"), name="password_reset"),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name="internal/password_reset_done.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="internal/password_reset_confirm.html"), name="password_reset_confirm"),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="internal/password_reset_complete.html"), name="password_reset_complete"),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name="internal/password_change.html"), name="password_change"),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name="internal/password_change_done.html"), name="password_change_done"),

    # bit-byte app
    path('profile/', views.profile_view, name='bitbyte_profile'),
    path('teams/', views.teams_view, name='bitbyte_teams'),
    path('teams/create/', views.teams_create_view, name='bitbyte_teams_create'),
    path('teams/join/', views.teams_join_view, name='bitbyte_teams_join'),
    path('events/', views.events_view, name='bitbyte_events'),
    path('events/submit/', views.events_submit_view, name='bitbyte_events_submit'),
    # path('edit/', views.edit, name='edit'),

    # # wiki
    # path('admin/', admin.site.urls),
    # # path('notifications/', include('django_nyt.urls')),
    # # path('challenge/', include('wiki.urls')),
    # path('challenge/', include('challenge.urls')),
    # path('accounts/login/', RedirectView.as_view(url='/login/')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('register/', views.register_view, name='register'),
    path('register/submit/', views.register_submit_view, name='register_submit'),
    path('login/', views.login_view, name='login'),
    path('login/submit/', views.login_submit_view, name='login_submit'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('teams/', views.teams_view, name='teams'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="internal/password_reset.html"), name="password_reset"),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name="internal/password_reset_done.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="internal/password_reset_confirm.html"), name="password_reset_confirm"),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="internal/password_reset_complete.html"), name="password_reset_complete"),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name="internal/password_change.html"), name="password_change"),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name="internal/password_change_done.html"), name="password_change_done"),
    path('events/', views.events_view, name='events'),
    path('events/submit/<int:prof_pk>/<int:event_pk>/', views.events_submit_view, name='events_submit'),
    # path('edit/', views.edit, name='edit'),
]
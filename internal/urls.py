from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('register/', views.register_view, name='register'),
    path('register/submit/', views.register_submit_view, name='register_submit'),
    path('login/', views.login_view, name='login'),
    path('login/submit/', views.login_submit_view, name='login_submit'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    # path('edit/', views.edit, name='edit'),
]
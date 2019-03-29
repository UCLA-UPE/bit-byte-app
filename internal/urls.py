from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('register/submit/', views.register_submit, name='register_submit'),
    path('login/', views.auth, name='auth'),
    path('login/submit/', views.auth_submit, name='auth_submit'),
    path('profile/', views.profile, name='profile'),
    # path('edit/', views.edit, name='edit'),
]
from django.urls import path, re_path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # wiki
    # path('admins/', admin.site.urls),
    path('notifications/', include('django_nyt.urls')),
    path('', include('wiki.urls')),
    # path('/accounts/login/', views.index_view),


    # path('', views.index_view, name='challenge_index'),
]

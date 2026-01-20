

from django.urls import path
from . import views


urlpatterns = [
    path('', views.base, name='base'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    #path('home/', views.home, name='home'),
    #path('profile/', views.profile, name='profile'),
]
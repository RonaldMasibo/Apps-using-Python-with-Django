

from django.urls import path
from . import views


urlpatterns = [
    path('', views.base, name='base'),
    path('register/', views.register, name='register'),
    path('login/', views.doLogin, name='login'),
    path('logout/', views.doLogout, name='logout'),
    path('main/', views.main, name='main'),
    #path('profile/', views.profile, name='profile'),
]
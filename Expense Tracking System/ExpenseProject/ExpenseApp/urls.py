

from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name="index"),
    path('login', views.login, name='login'),
    path('calculating',views.calculating, name='calculating'),
    path('logout', views.logout, name="logout"),
]



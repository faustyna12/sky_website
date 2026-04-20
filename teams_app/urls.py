from django.urls import path
from . import views

urlpatterns = [
    path('', views.team_list, name='teams'),
]

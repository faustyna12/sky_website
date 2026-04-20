from django.urls import path
from .views import teams_page

urlpatterns = [
    path('', teams_page, name='teams'),
]

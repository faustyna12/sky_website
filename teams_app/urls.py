from django.urls import path
from .views import teams_page, team_detail

urlpatterns = [
    path('', teams_page, name='teams'),
    path('<int:team_id>/', team_detail, name='team_detail'),
]

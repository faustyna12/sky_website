from django.urls import path
from . import views

urlpatterns = [
    # This empty string '' means http://127.0.0.1:8000/organisation/
    path('', views.org_map_view, name='org_map'),
    path('export/', views.export_teams_csv, name='export_teams_csv'),
]

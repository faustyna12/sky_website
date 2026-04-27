from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('profile/', views.user_profile, name='user_profile'), # New Link
]

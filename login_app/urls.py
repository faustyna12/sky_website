from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    # This maps to http://127.0.0.1:8000/login/
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # In your urls.py
]
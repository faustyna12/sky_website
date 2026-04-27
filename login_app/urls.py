from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    # Login Page
    path('', auth_views.LoginView.as_view(template_name='login_app/login.html'), name='login'),

    # Help Page (Matches line 102 in your error)
    path('help/', TemplateView.as_view(template_name='login_app/help.html'), name='help'),

    # Contact/Support Page (Matches line 103 in your error)
    path('contact_support/', TemplateView.as_view(template_name='login_app/contact.html'), name='contact_support'),

   
]
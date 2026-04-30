from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from django.contrib.auth import views as auth_views
def privacy_view(request):
    return render(request, 'privacy.html')

def support_view(request):
    return render(request, 'contact.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('privacy/', privacy_view, name='privacy'), 
    path('support/', support_view, name='contact'),
    path('organisation/', include('organisation_app.urls')),
    path('login/', include('login_app.urls')),
    path('forgot-password/', lambda r: render(r, 'login_app/forgot_password.html'), name='forgot_password'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('teams/', include('teams_app.urls')),
    path('dashboard/', include('sky_dash.urls')),
    path('messages/', include('messages_app.urls')),
    path('reports/', include('reports_app.urls')),
]

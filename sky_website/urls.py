from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('messages/', include('messages_app.urls')),
    path('login/', include('login_app.urls')),
    path('schedule/', include('schedule_app.urls')),
    path('report/', include('report_app.urls')),
    path('team/', include('team_app.urls')),
    path('organisation/', include('organisation_app.urls')),

]
=======
    path('organisation/', include('organisation_app.urls')),
    
        path('login/', auth_views.LoginView.as_view(template_name='login_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', include('dashb_app.urls')),
    ]
>>>>>>> a01f0d9 (completed login styling and initial dashboard structure)

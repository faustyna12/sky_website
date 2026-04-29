from django.shortcuts import render
from django.contrib.auth.models import User
from teams_app.models import Team
from organisation_app.models import Department

def reports_dashboard(request):
    total_users = User.objects.count()
    total_teams = Team.objects.count()
    total_departments = Department.objects.count()
    recent_users = User.objects.order_by('-date_joined')[:5]
    
    context = {
        'total_users': total_users,
        'total_teams': total_teams,
        'total_departments': total_departments,
        'recent_users': recent_users,
    }
    return render(request, 'reports_app/reports.html', context)
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from teams_app.models import Team
from organisation_app.models import Department

def reports_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_staff:
        return redirect('dashboard')
    
    search = request.GET.get('search', '')
    
    total_users = User.objects.count()
    total_teams = Team.objects.count()
    total_departments = Department.objects.count()
    recent_users = User.objects.order_by('-date_joined')[:5]
    
    if search:
        all_teams = Team.objects.filter(name__icontains=search)
    else:
        all_teams = Team.objects.all()
    
    context = {
        'total_users': total_users,
        'total_teams': total_teams,
        'total_departments': total_departments,
        'recent_users': recent_users,
        'all_teams': all_teams,
        'search': search,
    }
    return render(request, 'reports_app/reports.html', context)
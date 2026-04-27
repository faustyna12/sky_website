from django.shortcuts import render
from organisation_app.models import Team

def dashboard_home(request):
    # Fetching the 3 most recent teams to act as 'Recently Visited'
    recent_teams = Team.objects.select_related('department', 'team_type').all().order_by('-id')[:3]
    
    context = {
        'recent_teams': recent_teams,
        'user_name': request.user.first_name or request.user.username,
    }
    return render(request, 'sky_dash/sky_dash.html', context)
from django.shortcuts import render
from organisation_app.models import Team, Department

def dashboard_home(request):
    # Pull real teams from your loaded fixture data
    all_teams = Team.objects.all()
    recent_teams = all_teams.order_by('-id')[:3]
    
    # Authenticated user check to prevent the 'AnonymousUser' crash
    if request.user.is_authenticated:
        user_name = request.user.first_name or request.user.username
    else:
        user_name = "Guest"

    context = {
        'recent_teams': recent_teams,
        'total_teams_count': all_teams.count(),
        'user_name': user_name,
    }
    return render(request, 'sky_dash/sky_dash.html', context)
from django.contrib.auth.decorators import login_required

@login_required
def user_profile(request):
    return render(request, 'sky_dash/user_profile.html')
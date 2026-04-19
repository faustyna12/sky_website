from django.shortcuts import render
from django.urls import reverse
from .models import Team, Dependency

def team_list(request):
    query = request.GET.get('q', '')
    teams = Team.objects.all()
    
    if query:
        teams = teams.filter(name__icontains=query)
    
    for team in teams:
        team.upstream = Dependency.objects.filter(source_team=team, dependency_type='Upstream')
        team.downstream = Dependency.objects.filter(target_team=team, dependency_type='Downstream')
        team.schedule_url = reverse('schedule_meeting') + f'?team={team.id}'
    
    context = {
        'teams': teams,
        'query': query,
    }
    return render(request, 'teams_app/teams.html', context)

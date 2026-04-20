from django.shortcuts import render
from .models import Team

def team_list(request):
    teams = Team.objects.all()
    
    search = request.GET.get('search')
    skill = request.GET.get('skill')
    
    if search:
        teams = teams.filter(name__icontains=search)
    
    if skill:
        teams = teams.filter(skills__name__icontains=skill)
    
    return render(request, 'teams_app/teams.html', {'teams': teams})

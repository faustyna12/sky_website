from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from organisation_app.models import Team, Department, TeamType


def teams_page(request):
    teams = Team.objects.select_related('department', 'team_type').prefetch_related(
        'upstream_dependencies',
        'downstream_dependents'
    ).all()

    search = request.GET.get('search', '').strip()
    department = request.GET.get('department', '').strip()
    skill = request.GET.get('skill', '').strip()

    if search:
        teams = teams.filter(
            Q(name__icontains=search) |
            Q(specialization__icontains=search)
        )

    if department:
        teams = teams.filter(department__name=department)

    if skill:
        teams = teams.filter(
            Q(team_type__name__icontains=skill) |
            Q(specialization__icontains=skill)
        )

    total_dependencies = 0
    for team in teams:
        total_dependencies += team.upstream_dependencies.count()
        total_dependencies += team.downstream_dependents.count()

    return render(request, 'teams_app/teams.html', {
        'teams': teams,
        'departments': Department.objects.all(),
        'skills': TeamType.objects.all(),
        'total_dependencies': total_dependencies,
    })


def team_detail(request, team_id):
    team = get_object_or_404(
        Team.objects.select_related('department', 'team_type').prefetch_related(
            'upstream_dependencies',
            'downstream_dependents'
        ),
        id=team_id
    )

    return render(request, 'teams_app/team_detail.html', {
        'team': team
    })

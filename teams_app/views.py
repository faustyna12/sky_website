from django.shortcuts import render
from django.db.models import Q
from .models import Team, Skill


def teams_page(request):
    teams = Team.objects.prefetch_related(
        'members',
        'skills',
        'upstream',
        'downstream',
    ).all()

    departments = (
        Team.objects.exclude(department__isnull=True)
        .exclude(department__exact='')
        .values_list('department', flat=True)
        .distinct()
    )

    skills = Skill.objects.all().order_by('name')

    search = request.GET.get('search', '').strip()
    department = request.GET.get('department', '').strip()
    skill = request.GET.get('skill', '').strip()

    if search:
        teams = teams.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )

    if department:
        teams = teams.filter(department=department)

    if skill:
        teams = teams.filter(skills__name=skill)

    teams = teams.distinct()

    total_dependencies = 0
    for team in teams:
        total_dependencies += team.upstream.count()
        total_dependencies += team.downstream.count()

    context = {
        'teams': teams,
        'departments': departments,
        'skills': skills,
        'total_dependencies': total_dependencies,
    }

    return render(request, 'teams_app/teams.html', context)

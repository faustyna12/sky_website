from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Department, TeamType, Team
from django.db.models import Count
import csv
from django.http import HttpResponse

def export_teams_csv(request):
    # 1. Capture current filters from the URL
    selected_dept = request.GET.get('department', 'all')
    selected_type = request.GET.get('team_type', 'all')
    dep_filter = request.GET.get('dependencies', 'all').lower()

    # 2. Apply the exact same filtering logic as your map view
    teams = Team.objects.select_related('department', 'team_type').all()

    if selected_dept != 'all':
        teams = teams.filter(department_id=selected_dept)
    if selected_type != 'all':
        teams = teams.filter(team_type_id=selected_type)

    # 3. Create the HTTP Response with CSV headers
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sky_organisation_export.csv"'

    writer = csv.writer(response)
    # Write the Header Row
    writer.writerow(['Team Name', 'Department', 'Team Type', 'Members', 'Specialization'])

    # Write Data Rows
    for team in teams:
        writer.writerow([
            team.name, 
            team.department.name, 
            team.team_type.name, 
            team.members_count, 
            team.specialization
        ])

    return response
@login_required
def org_map_view(request):
    selected_dept = request.GET.get('department', 'all')
    selected_type = request.GET.get('team_type', 'all')
    dep_filter = request.GET.get('dependencies', 'all').lower()

    teams = Team.objects.select_related('department', 'team_type').all()

    if selected_dept != 'all':
        teams = teams.filter(department_id=selected_dept)
    
    if selected_type != 'all':
        teams = teams.filter(team_type_id=selected_type)

    if dep_filter == 'upstream':
        teams = teams.annotate(up_count=Count('upstream_dependencies')).filter(up_count__gt=0)
    elif dep_filter == 'downstream':
        teams = teams.filter(downstream_dependents__isnull=False).distinct()

    teams_dept_ids = list(teams.values_list('department_id', flat=True).distinct())
    display_departments = Department.objects.filter(id__in=teams_dept_ids).order_by('id')

    total_teams = teams.count()
    total_deps = sum(t.upstream_dependencies.count() for t in teams)

    context = {
        'departments': display_departments,
        'departments_list': Department.objects.all(),
        'team_types': TeamType.objects.all(),
        'teams': teams,
        'current_filter': dep_filter,
        'selected_dept': selected_dept,
        'selected_type': selected_type,
        'total_teams': total_teams,
        'total_deps': total_deps,
    }
    return render(request, 'organisation_app/organisation.html', context)
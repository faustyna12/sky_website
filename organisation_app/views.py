from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Department, TeamType, Team
from django.db.models import Count
import csv
from django.http import HttpResponse

def export_teams_csv(request):
    """
    Generates a downloadable CSV file based on the user's current filter selection.
    """
    # 1. Capture current filter parameters from the URL (defaults to 'all')
    selected_dept = request.GET.get('department', 'all')
    selected_type = request.GET.get('team_type', 'all')

    # 2. Query the database using select_related to join tables (optimizes performance)
    teams = Team.objects.select_related('department', 'team_type').all()

    # 3. Mirror the filtering logic used in the main view
    if selected_dept != 'all':
        teams = teams.filter(department_id=selected_dept)
    if selected_type != 'all':
        teams = teams.filter(team_type_id=selected_type)

    # 4. Initialize the HTTP Response as a file stream (CSV)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sky_organisation_export.csv"'

    # 5. Build the CSV content
    writer = csv.writer(response)
    # Define Header Row columns
    writer.writerow(['Team Name', 'Department', 'Team Type', 'Members', 'Specialization'])

    # Loop through filtered teams and write data rows
    for team in teams:
        writer.writerow([
            team.name, 
            team.department.name, 
            team.team_type.name, 
            team.members_count, 
            team.specialization
        ])

    return response


@login_required  # Ensures only logged-in users can access the Org Map
def org_map_view(request):
    """
    Main controller for the Organisation Map visualization.
    """
    # Retrieve filtering state from GET parameters
    selected_dept = request.GET.get('department', 'all')
    selected_type = request.GET.get('team_type', 'all')
    dep_filter = request.GET.get('dependencies', 'all').lower()

    # Fetch teams and their related data in one go to prevent "N+1" query issues
    teams = Team.objects.select_related('department', 'team_type').all()

    # --- Filtering Logic ---
    if selected_dept != 'all':
        teams = teams.filter(department_id=selected_dept)
    
    if selected_type != 'all':
        teams = teams.filter(team_type_id=selected_type)

    # Dependency specific filtering
    if dep_filter == 'upstream':
        # Annotate each team with count of dependencies and filter for those that have them
        teams = teams.annotate(up_count=Count('upstream_dependencies')).filter(up_count__gt=0)
    elif dep_filter == 'downstream':
        # Filter for teams that appear in the reverse relationship (downstream)
        teams = teams.filter(downstream_dependents__isnull=False).distinct()

    # Get a distinct list of Department IDs from the filtered teams to hide empty departments
    teams_dept_ids = list(teams.values_list('department_id', flat=True).distinct())
    display_departments = Department.objects.filter(id__in=teams_dept_ids).order_by('id')

    # --- Metrics for Sidebar ---
    total_teams = teams.count()
    # Calculate total connections (summing ManyToMany counts)
    total_deps = sum(t.upstream_dependencies.count() for t in teams)

    # Pack data into a dictionary for the template to use
    context = {
        'departments': display_departments,      # Departments containing filtered teams
        'departments_list': Department.objects.all(), # For the dropdown menu
        'team_types': TeamType.objects.all(),     # For the dropdown menu
        'teams': teams,                          # The filtered team objects
        'current_filter': dep_filter,
        'selected_dept': selected_dept,
        'selected_type': selected_type,
        'total_teams': total_teams,
        'total_deps': total_deps,
    }
    
    # Return the rendered HTML page with the context data
    return render(request, 'organisation_app/organisation.html', context)
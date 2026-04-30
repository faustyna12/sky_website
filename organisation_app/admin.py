from django.contrib import admin
from .models import Department, TeamType, Team

# --- Department Administration ---
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    # Sets which fields are visible as columns in the department list view
    list_display = ('name',)

# --- Team Type Administration ---
@admin.register(TeamType)
class TeamTypeAdmin(admin.ModelAdmin):
    # Displays the name and the associated hex/color code for the team category
    list_display = ('name', 'color_code')

# --- Team Administration ---
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    # Columns to display in the main list view for Teams
    list_display = ('name', 'team_type', 'department', 'members_count')
    
    # Adds a sidebar on the right to filter teams by Department or Type
    list_filter = ('department', 'team_type')
    
    # Adds a search bar at the top to query by name or specialized skill
    search_fields = ('name', 'specialization')
    
    # --- UI Enhancement ---
    # Changes the Many-to-Many selection from a standard multi-select box
    # to a side-by-side "Filter Horizontal" interface. 
    # Great for managing complex relationships (like upstream dependencies).
    filter_horizontal = ('upstream_dependencies',)
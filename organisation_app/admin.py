from django.contrib import admin
from .models import Department, TeamType, Team

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(TeamType)
class TeamTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'color_code')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'team_type', 'department', 'members_count')
    list_filter = ('department', 'team_type')
    search_fields = ('name', 'specialization')
    
    # This creates a nice UI for selecting dependencies
    filter_horizontal = ('upstream_dependencies',)
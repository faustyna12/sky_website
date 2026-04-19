from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = "Departments"

    def __str__(self):
        return self.name

class TeamType(models.Model):
    name = models.CharField(max_length=50, unique=True) # e.g., Backend, QA
    color_code = models.CharField(max_length=7, default="#3498db") # hex color for UI
    
    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100, help_text="e.g. Architecture or Mobile")
    members_count = models.PositiveIntegerField(default=1)
    
    # Relationships
    department = models.ForeignKey(
        Department, 
        on_delete=models.PROTECT, # Protect prevents deleting a Dept if it has teams
        related_name="teams"
    )
    team_type = models.ForeignKey(
        TeamType, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="teams"
    )
    
    # The Network Mapping logic
    # upstream_dependencies: Teams this team relies on
    upstream_dependencies = models.ManyToManyField(
        'self', 
        symmetrical=False, 
        related_name='downstream_dependents', 
        blank=True
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.team_type})"
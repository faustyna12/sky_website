from django.db import models

# --- Organization Hierarchy ---

class Department(models.Model):
    """
    Represents a high-level business unit (e.g., Engineering, Product).
    """
    # unique=True ensures no two departments share the same name
    name = models.CharField(max_length=100, unique=True)
    
    # Stores the name of the Executive/Head of Department
    leader = models.CharField(max_length=100, default="TBD")
    
    # TextField allows for long-form mission statements or specializations
    description = models.TextField(blank=True, help_text="Department specialization")

    class Meta:
        # Corrects the default Django pluralization ("Departments" vs "Departments")
        verbose_name_plural = "Departments"

    def __str__(self):
        # Returns the name in the Admin panel and shell
        return self.name


class TeamType(models.Model):
    """
    Categorizes teams by function (e.g., Frontend, DevOps, Security).
    """
    name = models.CharField(max_length=50, unique=True) 
    
    # Stores hex codes (e.g., #FFFFFF) to drive dynamic UI coloring in the frontend
    color_code = models.CharField(max_length=7, default="#3498db") 
    
    def __str__(self):
        return self.name


class Team(models.Model):
    """
    The central model representing a specific working group.
    """
    name = models.CharField(max_length=100)
    
    # Brief label describing the team's specific focus
    specialization = models.CharField(max_length=100, help_text="e.g. Architecture or Mobile")
    
    # Number of people in the team; PositiveIntegerField prevents negative headcount
    members_count = models.PositiveIntegerField(default=1)
    
    # --- Database Relationships ---
    
    # ForeignKey creates a Many-to-One link: Many teams belong to one department
    department = models.ForeignKey(
        Department, 
        on_delete=models.PROTECT, # Stops deletion of a Department if Teams still exist inside it
        related_name="teams"      # Allows access via department.teams.all()
    )
    
    # Link to TeamType; SET_NULL keeps the team record even if the 'type' category is deleted
    team_type = models.ForeignKey(
        TeamType, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="teams"
    )
    
    # --- Self-Referential Many-to-Many Relationship ---
    
    # This creates the 'Network' effect. 
    # symmetrical=False is crucial: if Team A relies on Team B, Team B doesn't 
    # automatically rely on Team A.
    upstream_dependencies = models.ManyToManyField(
        'self', 
        symmetrical=False, 
        related_name='downstream_dependents', # Creates the reverse link automatically
        blank=True
    )

    class Meta:
        # Ensures teams are always listed alphabetically in the UI
        ordering = ['name']

    def __str__(self):
        # Formats the object string for better readability in debugging
        return f"{self.name} ({self.team_type})"
from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    skills = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Dependency(models.Model):
    DEPENDENCY_TYPES = (
        ('Upstream', 'Upstream'),
        ('Downstream', 'Downstream'),
    )
    source_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='dependencies_as_source')
    target_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='dependencies_as_target')
    dependency_type = models.CharField(max_length=20, choices=DEPENDENCY_TYPES)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.source_team.name} -> {self.target_team.name} ({self.dependency_type})"

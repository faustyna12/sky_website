from django.db import models
from django.contrib.auth.models import User

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    description = models.TextField(blank=True)
    department = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    members = models.ManyToManyField(User, blank=True, related_name='teams')
    skills = models.ManyToManyField(Skill, blank=True, related_name='teams')
    repositories = models.IntegerField(default=0)
    upstream = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='downstream')
    calendar_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    def member_count(self):
        return self.members.count()

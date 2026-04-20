from django.db import models
from django.contrib.auth.models import User


class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)

    members = models.ManyToManyField(User, blank=True)
    skills = models.ManyToManyField(Skill, blank=True)

    upstream = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        related_name='downstream'
    )

    def __str__(self):
        return self.name

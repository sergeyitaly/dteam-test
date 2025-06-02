from django.db import models

class Skill(models.Model):
    name = models.CharField(max_length=100)
    proficiency = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f"{self.name} ({self.proficiency}/5)"

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    year = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.title

class CV(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField()
    skills = models.ManyToManyField(Skill, blank=True)
    projects = models.ManyToManyField(Project, blank=True)
    contacts = models.JSONField(default=dict)  # Stores email, phone, LinkedIn, etc.
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
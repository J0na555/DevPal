from django.db import models
from users.models import UserProfile

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    tech_stack = models.JSONField(default=list)
    needed_roles = models.JSONField(default=list)
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    members = models.ManyToManyField(UserProfile, related_name="projects_joined", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

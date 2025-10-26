from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField


User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    skills = ArrayField(models.CharField(max_length=50), default=list )
    interests = ArrayField(models.CharField(max_length=50), default=list)
    availability_hours = models.IntegerField(default=10)
    preferred_roles = ArrayField(models.CharField(max_length=50), default=list)

    def __str__(self):
        return getattr(self.user, 'username', str(self.pk))
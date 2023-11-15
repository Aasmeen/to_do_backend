from django.contrib.auth.models import User
from django.db import models


class Tasks(models.Model):
    title = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False)
    is_important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule = models.DateTimeField(null=True, blank=True)
    reminder = models.DateTimeField(null=True, blank=True)

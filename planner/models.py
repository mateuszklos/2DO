from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class Task(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=datetime.now)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

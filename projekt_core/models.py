from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User


# Projects
class Project(models.Model):
    title = models.CharField(unique=True, max_length=256)
    owner = models.ForeignKey(User, unique=False, blank=True,
                                null=True, on_delete=models.CASCADE)

    finished = models.BooleanField(default=False)
    time_spent = models.DurationField(default=timedelta(0))

    def __str__(self):
        return self.title

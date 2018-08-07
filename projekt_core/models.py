import random
from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


# Funkcje pomocnicze
def get_random_color():
    colors = ['red', 'green', 'blue', 'orange', 'purple']
    return random.choice(colors)


def create_step(project, step_title):
    step = Step()

    step.title = step_title;
    step.project = project

    step.save()

    project.step_set.add(step)


# Projects
class Project(models.Model):
    title = models.CharField(unique=True, max_length=256)
    owner = models.ForeignKey(User, unique=False, blank=True,
                                null=True, on_delete=models.CASCADE)

    finished = models.BooleanField(default=False)
    time_spent = models.DurationField(default=timedelta(0))

    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


# Step
class Step(models.Model):
    title = models.CharField(unique=True, max_length=128)
    project = models.ForeignKey(Project, blank=True, null=True,
                                on_delete=models.CASCADE)

    color = models.CharField(max_length=10)
    time_spent = models.DurationField(default=timedelta(0))

    def save(self, *args, **kwargs):
        if not self.id:
            self.color = get_random_color()
            self.title = slugify(self.title)
        super(Step, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

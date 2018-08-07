import random
from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.shortcuts import get_object_or_404


# Funkcje pomocnicze
def get_random_color():
    colors = ['red', 'green', 'blue', 'orange', 'purple']
    return random.choice(colors)

def preslugify(step_title):
    if len(Step.objects.all().filter(title=step_title)) > 0:
        new_title = step_title
        while len(Step.objects.all().filter(title=new_title)) > 0:
            new_title = "{}{}".format(step_title, random.randint(1, 10000))
        return new_title
    return step.title

def create_step(project, step_title):
    project.step_set.create(title=step_title)

def remove_step(project, step_title):
    steps = Step.objects.all().filter(project=project, title=step_title)
    for step in steps:
        step.delete()


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
    title = models.CharField(unique=False, max_length=128)
    project = models.ForeignKey(Project, blank=True, null=True,
                                on_delete=models.CASCADE)

    color = models.CharField(max_length=10)
    time_spent = models.DurationField(default=timedelta(0))

    def save(self, *args, **kwargs):
        if not self.id:
            self.title = preslugify(self.title);
            self.color = get_random_color()
            self.title = slugify(self.title)
        super(Step, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

import random
from datetime import timedelta, datetime, timezone

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.shortcuts import get_object_or_404


# Funkcje pomocnicze
def get_random_color():
    colors = ['orange', 'green', 'blue', 'purple', 'red', 'green', 'blue', 'orange', 'purple']
    return random.choice(colors)

def preslugify(step_title):
    if len(Step.objects.all().filter(title=step_title)) > 0:
        new_title = step_title
        while len(Step.objects.all().filter(title=new_title)) > 0:
            new_title = "{}{}".format(step_title, random.randint(1, 10000))
        return new_title
    return step_title

# steps
def create_step(project, step_title):
    project.step_set.create(title=step_title)

def remove_step(project, step_title):
    steps = Step.objects.all().filter(project=project, title=step_title)
    for step in steps:
        step.delete()

# tasks
def create_task(project, step_title, task_title):
    step = get_object_or_404(project.step_set.all(), title=step_title)
    step.task_set.create(title=task_title)

def activate_task(project, step_title, task_title):
    step = get_object_or_404(project.step_set.all(), title=step_title)
    task = step.task_set.get(title=task_title)

    task.activate()

def deactivate_task(project, step_title, task_title):
    step = get_object_or_404(project.step_set.all(), title=step_title)
    task = step.task_set.get(title=task_title)
    task = get_object_or_404(step.task_set.all(), title=task_title)

    task.deactivate()

def move_task(project, step_title_form, step_title_to, task_title):
    step_to = project.step_set.get(title=step_title_to)
    step_from = project.step_set.get(title=step_title_form)

    task = step_from.task_set.get(title=task_title)

    if step_to == None or step_from == None or task == None:
        return

    step_to.task_set.create(title=task.title, time_spent=task.time_spent,
                                active=task.active, activation_date=task.activation_date)
    task.delete()

def remove_task(project, step_title, task_title):
    steps = Step.objects.all().filter(project=project, title=step_title)
    for step in steps:
        for task in step.task_set.all().filter(title=task_title):
            task.delete()

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

    def recalculate_time_spent(self):
        self.time_spent = timedelta(0);

        for step in self.step_set.all():
            for task in step.task_set.all():
                self.time_spent += task.time_spent

    def __str__(self):
        self.recalculate_time_spent()
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
        super(Step, self).save(*args, **kwargs)

    def recalculate_time_spent(self):
        self.time_spent = timedelta(0);
        for task in self.task_set.all():
            self.time_spent += task.time_spent

    def __str__(self):
        self.recalculate_time_spent(    )
        return self.title


# Task
class Task(models.Model):
    title = models.CharField(unique=False, max_length=128)
    step = models.ForeignKey(Step, blank=True, null=True,
                                on_delete=models.CASCADE)

    active = models.BooleanField(default=False)
    activation_date = models.DateTimeField(blank=True, null=True)

    color = models.CharField(max_length=10)
    time_spent = models.DurationField(default=timedelta(0))

    def save(self, *args, **kwargs):
        if not self.id:
            self.title = preslugify(self.title);
            self.color = get_random_color()
        super(Task, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    # get time passed
    # since activation
    def activate(self):
        if self.active == True:
            return
        self.active = True
        self.activation_date = datetime.now(timezone.utc)
        self.save()

    def deactivate(self):
        if self.active == True:
            time_delta = datetime.now(timezone.utc) - self.activation_date
            self.time_spent += time_delta
            self.active = False
        self.save()

from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


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

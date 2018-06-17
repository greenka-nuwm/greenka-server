from django.db import models
from django.contrib.auth.models import User


class ProblemType(models.Model):
    """Object that represents type of problems."""
    name = models.CharField(max_length=64, unique=True)
    verbose_name = models.CharField(max_length=128, unique=True)
    description = models.TextField(max_length=4096)
    is_active = models.BooleanField(default=True)


class ProblemState(models.Model):
    """Object that represents problem state."""
    name = models.CharField(max_length=64, unique=True)
    verbose_name = models.CharField(max_length=128, unique=True)
    description = models.TextField(max_length=4096)
    is_active = models.BooleanField(default=True)


class Problem(models.Model):
    """Problem object class."""
    latitude = models.FloatField()
    longitude = models.FloatField()

    problem_type = models.ForeignKey(ProblemType, blank=False, null=False, on_delete=models.CASCADE)
    problem_state = models.ForeignKey(ProblemState, blank=False, null=False, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)
    approved = models.BooleanField(default=False)
    confirms = models.ManyToManyField(User, 'confirms')

    reporter = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)

    creation_time = models.DateTimeField(auto_now_add=True)
    modification_time = models.DateTimeField(auto_now=True)

    description = models.TextField(max_length=4096, blank=True, null=True)


class ProblemImage(models.Model):
    """Image object for problems."""
    url = models.ImageField(upload_to="static/img", max_length=128, unique=True)
    problem = models.ForeignKey(Problem, blank=False, null=False, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

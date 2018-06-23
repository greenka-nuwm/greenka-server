from django.db import models
from django.contrib.auth.models import User


class Feedback(models.Model):
    """Class to describe feedback about application from users."""

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    is_active = models.BooleanField(default=True)

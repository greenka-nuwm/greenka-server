from django.db import models
from django.contrib.auth.models import User, AbstractUser

from greenka import settings

from tree.models import Tree
from problems.models import Problem


class User(AbstractUser):
    profile_image = models.ImageField(
        upload_to="static/img", max_length=128)
    profile_background_image = models.ImageField(
        upload_to="static/img", max_length=128)


class Feedback(models.Model):
    """Class to describe feedback about application from users."""

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    body = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'feedback'


class FeedbackImage(models.Model):
    """Contain path to image attached to specific feedback."""
    url = models.ImageField(upload_to="static/img", max_length=128, unique=True)
    feedback = models.ForeignKey('Feedback', related_name='images', on_delete=models.CASCADE)
    visible = models.BooleanField(default=False)

    def __str__(self):
        return '/' + str(self.url.path)

    class Meta:
        db_table = 'feedback_image'

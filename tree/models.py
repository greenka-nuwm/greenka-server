# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class TreeType(models.Model):
    """Type of tree."""
    name = models.CharField(max_length=64)


class TreeSort(models.Model):
    """Sort of tree, also know about itself type."""
    name = models.CharField(max_length=128)
    tree_type = models.ForeignKey('TreeType',
                                  on_delete=models.CASCADE)


class Tree(models.Model):
    """Tree object."""
    (HEALTHY, DRY, BROKEN,
     TOPING, MISTLETOE, DYING, ) = range(6)

    STATES = (
        (HEALTHY, 'HEALTHY'),
        (DRY, 'DRY'),
        (BROKEN, 'BROKEN'),
        (TOPING, 'TOPING'),
        (MISTLETOE, 'MISTLETOE'),
        (DYING, 'DYING'),
    )

    latitude = models.FloatField()
    longitude = models.FloatField()

    tree_state = models.IntegerField(choices=STATES)

    tree_type = models.ForeignKey('TreeType', blank=True,
                                  null=True,
                                  on_delete=models.SET_NULL)
    tree_sort = models.ForeignKey('TreeSort', blank=True,
                                  null=True,
                                  on_delete=models.SET_NULL)

    description = models.TextField(blank=True)

    owner = models.ForeignKey(User,
                              related_name='trees',
                              on_delete=models.SET(get_sentinel_user))

    active = models.BooleanField(default=True)
    visible = models.BooleanField(default=True)

    approved = models.BooleanField(default=False)
    confirms = models.ManyToManyField(User)


class TreeImages(models.Model):
    """Contain path to image attached to specific tree."""
    url = models.ImageField(upload_to="static/img", max_length=128, unique=True)
    tree = models.ForeignKey('Tree', related_name='images', on_delete=models.CASCADE)
    visible = models.BooleanField(default=False)

    def __str__(self):
        return '/' + str(self.url.path)


class Polygon(models.Model):
    name = models.CharField(unique=True, max_length=128)
    description = models.TextField()


class PolyPoint(models.Model):
    poly = models.ForeignKey('Polygon', related_name='points', on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()

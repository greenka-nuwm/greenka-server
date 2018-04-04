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

    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long = models.DecimalField(max_digits=9, decimal_places=6)

    tree_state = models.IntegerField(choices=STATES)

    tree_type = models.ForeignKey('TreeType', blank=True,
                                  null=True,
                                  on_delete=models.SET_NULL)
    tree_sort = models.ForeignKey('TreeSort', blank=True,
                                  null=True,
                                  on_delete=models.SET_NULL)

    description = models.TextField(blank=True)

    owner = models.ForeignKey(User,
                              on_delete=models.SET(get_sentinel_user))

    active = models.BooleanField(default=True)
    visible = models.BooleanField(default=True)

    approved = models.BooleanField(default=False)
    confirms = models.IntegerField(default=1)


class TreeImages(models.Model):
    """Contain path to image attached to specific tree."""
    url = models.ImageField(upload_to="static/img", max_length=128)
    tree = models.ForeignKey('Tree', on_delete=models.CASCADE)
    visible = models.BooleanField(default=False)

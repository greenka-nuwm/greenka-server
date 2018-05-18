import tree.views as tree_views

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path(r'all', tree_views.get_trees),
]


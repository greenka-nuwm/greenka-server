from django.contrib import admin
from tree.models import Tree


@admin.register(Tree)
class TreeAdmin(admin.ModelAdmin):
    pass
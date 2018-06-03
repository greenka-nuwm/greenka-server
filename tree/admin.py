from django.contrib import admin
from tree.models import Tree, TreeSort, TreeType


@admin.register(Tree)
class TreeAdmin(admin.ModelAdmin):
    pass


@admin.register(TreeType)
class TreeTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(TreeSort)
class TreeSortAdmin(admin.ModelAdmin):
    pass
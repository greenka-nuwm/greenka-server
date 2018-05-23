import tree.views as tree_views
from django.contrib import admin
from django.urls import include, path, register_converter
from tree.converters import FloatConverter


register_converter(FloatConverter, 'float')


urlpatterns = [
    path(r'<float:lat>,<float:lng>/<str:distance>', tree_views.TreeListReadOnlyView.as_view()),
    path(r'', tree_views.TreeAddView.as_view()),
    path(r'all', tree_views.get_trees),
]

import tree.views as tree_views

from django.contrib import admin
from django.urls import include, path, register_converter
from tree.converters import FloatConverter


register_converter(FloatConverter, 'float')

poly = [
    path(r'', tree_views.PolygonListCreateView.as_view()),
    path(r'<int:pk>', tree_views.PolygonDetailsView.as_view()),
]

types = [
    path(r'', tree_views.TreeTypeListCreateView.as_view()),
    path(r'<int:pk>', tree_views.TreeTypeDetailsView.as_view()),
]

sorts = [
    path(r'', tree_views.TreeSortListCreateView.as_view()),
    path(r'<int:pk>', tree_views.TreeSortDetailsView.as_view()),
]

urlpatterns = [
    path('poly/', include(poly)),
    path('types/', include(types)),
    path('sorts/', include(sorts)),
    path(r'<int:pk>', tree_views.TreeDetailsReadOnlyView.as_view()),
    path(r'<int:pk>/confirm', tree_views.confirm_tree),
    path(r'<int:pk>/approve', tree_views.set_approve_tree),
    path(r'', tree_views.TreeAddView.as_view()),
    path(r'all', tree_views.get_trees),
    path(r'<int:pk>/image/', tree_views.TreeImageCreateView.as_view()),
]

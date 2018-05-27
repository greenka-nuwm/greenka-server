import tree.views as tree_views
from django.contrib import admin
from django.urls import include, path, register_converter
from tree.converters import FloatConverter


register_converter(FloatConverter, 'float')


urlpatterns = [
    path(r'<float:lat>,<float:lng>/<str:distance>', tree_views.TreeListReadOnlyView.as_view()),
    path(r'<int:pk>', tree_views.TreeDetailsReadOnlyView.as_view()),
    path(r'<int:pk>/confirm', tree_views.confirm_tree),
    path(r'', tree_views.TreeAddView.as_view()),
    path(r'all', tree_views.get_trees),
    path(r'<int:pk>/image/', tree_views.TreeImageCreateView.as_view()),
    path(r'poly/', tree_views.PolygonListCreateView.as_view()),
    path(r'poly/<int:pk>', tree_views.PolygonDetailsView.as_view()),
    path(r'poly/<int:poly_pk>/get', tree_views.obtain_trees_in_polygon),
]

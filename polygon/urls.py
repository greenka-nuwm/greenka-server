from django.urls import path
from polygon.views import PolygonListCreateView, PolygonDetailsView


urlpatterns = [
    path(r'', PolygonListCreateView.as_view()),
    path(r'<int:pk>', PolygonDetailsView.as_view()),
]
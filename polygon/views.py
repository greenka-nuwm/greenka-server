from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from polygon.models import Polygon
from tree.permissions import IsAdminOrReadOnly
from polygon.serializers import PolygonSerializer


class PolygonListCreateView(generics.ListCreateAPIView):
    queryset = Polygon.objects.all()
    serializer_class = PolygonSerializer
    permission_classes = (IsAdminOrReadOnly, )


class PolygonDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Polygon.objects.all()
    serializer_class = PolygonSerializer
    permission_classes = (IsAdminUser, )
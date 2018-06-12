from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from polygon.models import Polygon
from tree.permissions import IsAdminOrReadOnly
from polygon.serializers import PolygonSerializer, PolygonGETSerializer


class PolygonListCreateView(generics.ListCreateAPIView):
    queryset = Polygon.objects.all()
    permission_classes = (IsAdminOrReadOnly, )

    def get_serializer_class(self):
        return PolygonGETSerializer
        # if self.request.method == 'GET':
        #     return PolygonGETSerializer
        # else:
        return PolygonSerializer


class PolygonDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Polygon.objects.all()
    serializer_class = PolygonSerializer
    permission_classes = (IsAdminUser, )
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAdminUser

from polygon.models import Polygon
from tree.permissions import IsAdminOrReadOnly
from polygon.serializers import PolygonSerializer, PolygonGETSerializer


class PolygonListCreateView(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication, )
    queryset = Polygon.objects.all()
    permission_classes = (IsAdminOrReadOnly, )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PolygonGETSerializer
        return PolygonSerializer


class PolygonDetailsView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication, )
    queryset = Polygon.objects.all()
    serializer_class = PolygonSerializer
    permission_classes = (IsAdminUser, )

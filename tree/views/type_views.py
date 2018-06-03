from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from tree.models import TreeType
from tree.permissions import IsAdminOrReadOnly
from tree.serializers import TreeTypeSerializer


class TreeTypeListCreateView(generics.ListCreateAPIView):
    queryset = TreeType.objects.all()
    serializer_class = TreeTypeSerializer
    permission_classes = (IsAdminOrReadOnly, )


class TreeTypeDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TreeType.objects.all()
    serializer_class = TreeTypeSerializer
    permission_classes = (IsAdminUser, )
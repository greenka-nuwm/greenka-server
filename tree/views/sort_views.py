from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from tree.models import TreeSort
from tree.permissions import IsAdminOrReadOnly
from tree.serializers import TreeSortSerializer


class TreeSortListCreateView(generics.ListCreateAPIView):
    queryset = TreeSort.objects.all()
    serializer_class = TreeSortSerializer
    permission_classes = (IsAdminOrReadOnly, )


class TreeSortDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TreeSort.objects.all()
    serializer_class = TreeSortSerializer
    permission_classes = (IsAdminUser, )

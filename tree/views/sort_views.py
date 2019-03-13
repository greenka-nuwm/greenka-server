from rest_framework import generics
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAdminUser

from tree.models import TreeSort
from tree.permissions import IsAdminOrReadOnly
from tree.serializers import TreeSortSerializer


class TreeSortListCreateView(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication, )
    permission_classes = (IsAdminOrReadOnly, )
    queryset = TreeSort.objects.all()
    serializer_class = TreeSortSerializer


class TreeSortDetailsView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication, )
    permission_classes = (IsAdminUser, )
    queryset = TreeSort.objects.all()
    serializer_class = TreeSortSerializer

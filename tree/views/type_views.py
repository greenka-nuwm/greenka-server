from rest_framework import generics
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAdminUser

from tree.models import TreeType
from tree.permissions import IsAdminOrReadOnly
from tree.serializers import TreeTypeSerializer


class TreeTypeListCreateView(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication, )
    permission_classes = (IsAdminOrReadOnly, )
    queryset = TreeType.objects.all()
    serializer_class = TreeTypeSerializer


class TreeTypeDetailsView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication, )
    permission_classes = (IsAdminUser, )
    queryset = TreeType.objects.all()
    serializer_class = TreeTypeSerializer

from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BaseAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView

from tree.models import Tree
from tree.serializers import TreeSerializer, UserSerializer
from tree.helpers import get_range


@api_view(['GET'])
@authentication_classes((TokenAuthentication, ))
@permission_classes((IsAuthenticated, ))
def get_trees(request):
    """Return all user created trees"""
    trees = Tree.objects.filter(owner__exact=request.user.id).all()
    serializer = TreeSerializer(trees, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes((TokenAuthentication, ))
@permission_classes((IsAuthenticated, ))
def get_user(request):
    """Return info about self"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class TreeAddView(generics.CreateAPIView):
    queryset = Tree.objects.all()
    serializer_class = TreeSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TreeListReadOnlyView(APIView):

    def get(self, request, lat, lng, distance, format=None):
        query = get_range(Tree, lat, lng, distance).all()
        serializer = TreeSerializer(query, many=True)
        return Response(serializer.data)


class TreeDetailsReadOnlyView(generics.RetrieveAPIView):
    pass

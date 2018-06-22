from django.contrib.auth.models import UserManager
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from gauth.serializers import UserSerializer
from problems.models import Problem
from problems.serializers import ProblemGETSerializer
from tree.models import Tree
from tree.serializers import TreeGETSerializer


@api_view(['POST'])
@authentication_classes((TokenAuthentication, ))
@permission_classes((AllowAny, ))
def register(request):
    """Register new user in system.

    Required username and password
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes((TokenAuthentication, ))
@permission_classes((IsAuthenticated, ))
def get_self_profile(request):
    """Return info about self. No additional params need."""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes((TokenAuthentication, ))
@permission_classes((IsAuthenticated, ))
def get_self_trees(request):
    """Return all trees reported by user."""
    serializer = TreeGETSerializer(Tree.objects.filter(owner=request.user),
                                   many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes((TokenAuthentication, ))
@permission_classes((IsAuthenticated, ))
def get_self_problems(request):
    """Return all problems reported by user."""
    serializer = ProblemGETSerializer(Problem.objects.filter(reporter=request.user),
                                   many=True)
    return Response(serializer.data)
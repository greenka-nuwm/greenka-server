from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BaseAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from tree.models import Tree
from tree.serializers import TreeSerializer


@api_view(['GET'])
@authentication_classes((TokenAuthentication, ))
@permission_classes((IsAuthenticated, ))
def get_trees(request):
    """Return all user created trees"""
    trees = Tree.objects.filter(owner__exact=request.user.id).all()
    serializer = TreeSerializer(trees, many=True)
    return JsonResponse(serializer.data, safe=False)

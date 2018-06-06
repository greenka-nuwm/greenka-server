from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


from problems.filters import chain_filter_it, ProblemFilterException
from problems.models import Problem
from problems.serializers import ProblemSerializer


@api_view(['GET'])
@authentication_classes((TokenAuthentication, ))
def get_problems(request):
    try:
        result = chain_filter_it(request, Problem)
    except ProblemFilterException as error:
        return Response({'message': error.message})
    serializer = ProblemSerializer(result, many=True)
    return Response(serializer.data)
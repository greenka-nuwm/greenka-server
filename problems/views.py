from uuid import uuid4

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from django.shortcuts import get_object_or_404

from problems.filters import chain_filter_it, ProblemFilterException
from problems.models import Problem, ProblemState, ProblemType, ProblemPhoto
from problems import serializers
from problems.permissions import IsAdminOrReporterOrReadOnly


class ProblemView(generics.ListCreateAPIView):
    """# Create new problem or obtain list of problems.

    get:


    Return filtered list of problems.

    TODO: added filters description.


    post:

    Required fields:

    * verbose_name _(human readable name)_
    * latitude
    * longitude
    * description _(long description of the problem)_
    * problem_type _(problem type ID. See: [TYPES](/problems/types/))_
    """
    queryset = Problem.objects.all()
    serializer_class = serializers.ProblemSerializer
    authentication_classes = (TokenAuthentication, )

    def post(self, request, *args, **kwargs):
        if not IsAuthenticated().has_permission(request, self):
            raise NotAuthenticated()
        return super(ProblemView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            if not IsAdminUser().has_permission(request, self):
                queryset = queryset.filter(is_active=True)
            result = chain_filter_it(request, queryset)
        except ProblemFilterException as error:
            return Response({'message': error.message})
        serializer = serializers.ProblemSerializer(result, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user,
                        problem_state=ProblemState.objects.get(pk=1))


class ProblemRUDView(generics.RetrieveUpdateDestroyAPIView):
    """Obtain details about problem."""
    queryset = Problem.objects.filter(is_active=True)
    serializer_class = serializers.ProblemSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAdminOrReporterOrReadOnly, )


class ProblemTypeView(generics.ListCreateAPIView):
    queryset = ProblemType.objects.all()
    serializer_class = serializers.ProblemTypeSerializer
    authentication_classes = (TokenAuthentication, )

    def post(self, request, *args, **kwargs):
        if not IsAdminUser().has_permission(request, self):
            raise PermissionDenied()
        return super(ProblemTypeView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # hide not active types from common users.
        if not request.user or not request.user.is_staff:
            self.queryset = self.queryset.filter(is_active=True)
        return super(ProblemTypeView, self).get(request, *args, **kwargs)


class ProblemTypeRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProblemType.objects.all()
    serializer_class = serializers.ProblemTypeSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAdminUser, )


class ProblemStateView(generics.ListCreateAPIView):
    queryset = ProblemState.objects.all()
    serializer_class = serializers.ProblemStateSerializer
    authentication_classes = (TokenAuthentication, )

    def post(self, request, *args, **kwargs):
        if not IsAdminUser().has_permission(request, self):
            raise PermissionDenied()
        return super(ProblemStateView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # hide not active states from common users.
        if not request.user or not request.user.is_staff:
            self.queryset = self.queryset.filter(is_active=True)
        return super(ProblemStateView, self).get(request, *args, **kwargs)


class ProblemStateRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProblemState.objects.all()
    serializer_class = serializers.ProblemStateSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAdminUser, )

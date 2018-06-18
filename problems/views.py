from uuid import uuid4

from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from greenka.helpers import save_problem_image
from problems import serializers
from problems.filters import ProblemFilterException, chain_filter_it
from problems.models import Problem, ProblemImage, ProblemState, ProblemType
from problems.permissions import (IsAdminOrReporterOrReadOnly,
                                  IsProblemReporterOrAdminOrReadOnly)


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

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.ProblemGETShortSerializer
        return serializers.ProblemSerializer


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
        print(self.get_serializer(result, many=True))
        serializer = self.get_serializer(result, many=True)
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

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.ProblemGETSerializer
        return serializers.ProblemSerializer


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


class ProblemImageCreateView(APIView):
    """Add image."""
    queryset = ProblemImage.objects.all()
    serializer_class = serializers.ProblemImageSerializer
    permission_classes = (IsAuthenticated, IsProblemReporterOrAdminOrReadOnly, )
    parser_classes = (MultiPartParser, FormParser, )

    def post(self, request, pk):
        try:
            problem_obj = Problem.objects.get(pk=pk)
        except Exception:
            return Response({'error': 'Wrong problem ID.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if not IsProblemReporterOrAdminOrReadOnly().has_object_permission(request, self, problem_obj):
            raise PermissionDenied()

        img = request.data.get('img')
        if not img:
            return Response({'error': 'No `img` data found.'},
                            status=status.HTTP_400_BAD_REQUEST)
        # save image data on disk
        url = save_problem_image(img, problem_obj)
        serializer = serializers.ProblemImageSerializer(data={})
        if serializer.is_valid():
            try:
                serializer.save(url=url, visible=True, tree=problem_obj)
            except IntegrityError:
                return Response({'error': 'This image already exists.'},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

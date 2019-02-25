from django.contrib.auth.models import UserManager
from rest_framework import exceptions as exc
from rest_framework import generics
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import gauth.serializers as gauth_serializers
from gauth.models import Feedback, FeedbackImage
from gauth.permissions import IsFeedbackOwner, IsFeedbackImageOwner
from gauth.serializers import FeedbackImageSerializer
from greenka.helpers import save_feedback_image
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
    serializer = gauth_serializers.UserSerializer(data=request.data)
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
    serializer = gauth_serializers.UserGETSerializer(request.user)
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


class FeedbackView(generics.ListCreateAPIView):
    """View to leave feedback and watch own leaved feedbacks."""
    queryset = Feedback.objects.filter(is_active=True)
    serializer_class = gauth_serializers.FeedbackSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class FeedbackImageView(APIView):
    """Add image to feedback view."""
    queryset = FeedbackImage.objects.all()
    serializer_class = gauth_serializers.FeedbackImageSerializer
    permission_classes = (IsAuthenticated, IsFeedbackOwner, )
    parser_classes = (MultiPartParser, FormParser, )

    def post(self, request, pk):
        try:
            feedback_obj = Feedback.objects.get(pk=pk)
        except Exception:
            return Response({'error': 'Wrong tree ID.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if not IsFeedbackImageOwner().has_object_permission(request, self, feedback_obj):
            raise exc.PermissionDenied()

        img = request.data.get('img')
        if not img:
            return Response({'error': 'No `img` data found.'},
                            status=status.HTTP_400_BAD_REQUEST)
        # save image data on disk
        url = save_feedback_image(img, feedback_obj)
        serializer = FeedbackImageSerializer(data={})
        if serializer.is_valid():
            try:
                serializer.save(url=url, visible=True, feedback=feedback_obj)
            except IntegrityError:
                return Response({'error': 'This image already exists.'},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


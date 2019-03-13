from django.contrib.auth.models import UserManager
from django.core.exceptions import ValidationError
from rest_framework import exceptions as exc
from rest_framework import generics
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import gauth.serializers as gauth_serializers
from gauth.models import Feedback, FeedbackImage, User
from gauth.permissions import IsFeedbackOwner, IsFeedbackImageOwner
from gauth.serializers import FeedbackImageSerializer, UserProfileImageSerializer, UserBackgroundImageSerializer
from greenka.helpers import save_feedback_image, default_auth_classes, save_user_image
from problems.models import Problem
from problems.serializers import ProblemGETSerializer
from tree.models import Tree
from tree.serializers import TreeGETSerializer



@api_view(['POST'])
@default_auth_classes
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


@api_view(['GET', 'POST'])
@default_auth_classes
@permission_classes((IsAuthenticated, ))
def self_profile(request):
    """# Get info about self or edit it.
    
    **GET**:

    Return information about profile.

    **POST**:

    Update profile information. Editable fields:

    - first_name
    - last_name
    - email
    """
    if request.method == 'GET':
        serializer = gauth_serializers.UserGETSerializer(request.user)
        return Response(serializer.data)
    else:
        # edit data
        serializer = gauth_serializers.UserEditSerializer(request.user,
                                                          data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({'error': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@default_auth_classes
@permission_classes((IsAuthenticated, ))
def get_self_trees(request):
    """Return all trees reported by user."""
    serializer = TreeGETSerializer(Tree.objects.filter(owner=request.user),
                                   many=True)
    return Response(serializer.data)


@api_view(['GET'])
@default_auth_classes
@permission_classes((IsAuthenticated, ))
def get_self_problems(request):
    """Return all problems reported by user."""
    serializer = ProblemGETSerializer(Problem.objects.filter(reporter=request.user),
                                      many=True)
    return Response(serializer.data)


class FeedbackView(generics.ListCreateAPIView):
    """View to leave feedback and watch own leaved feedbacks."""
    authentication_classes = (TokenAuthentication, SessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = Feedback.objects.filter(is_active=True)
    serializer_class = gauth_serializers.FeedbackSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProfileBackgroundImageView(APIView):
    """Add image to feedback view."""
    authentication_classes = (TokenAuthentication, SessionAuthentication, )
    parser_classes = (MultiPartParser, FormParser, )
    permission_classes = (IsAuthenticated, IsFeedbackOwner, )

    def post(self, request):
        img = request.data.get('img')
        if not img:
            return Response({'error': 'No `img` data found.'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            url = save_user_image(img, request.user)
            if not url:
                raise IOError
        except (ValidationError, ValueError) as error:
            return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        except IOError:
            return Response({'error': 'Cannot set image, looks like it`s corrupted.'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = UserBackgroundImageSerializer(request.user, data={})
        if serializer.is_valid():
            serializer.save(profile_background_image=url)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileImageView(APIView):
    """Add image to feedback view."""
    authentication_classes = (TokenAuthentication, SessionAuthentication, )
    parser_classes = (MultiPartParser, FormParser, )
    permission_classes = (IsAuthenticated, IsFeedbackOwner, )

    def post(self, request):
        img = request.data.get('img')
        if not img:
            return Response({'error': 'No `img` data found.'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            url = save_user_image(img, request.user)
            if not url:
                raise IOError
        except (ValidationError, ValueError) as error:
            return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        except IOError:
            return Response({'error': 'Cannot set image, looks like it`s corrupted.'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = UserProfileImageSerializer(request.user, data={})
        if serializer.is_valid():
            serializer.save(profile_image=url)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FeedbackImageView(APIView):
    """Add image to feedback view."""
    authentication_classes = (TokenAuthentication, SessionAuthentication, )
    parser_classes = (MultiPartParser, FormParser, )
    permission_classes = (IsAuthenticated, IsFeedbackOwner, )
    queryset = FeedbackImage.objects.all()
    serializer_class = gauth_serializers.FeedbackImageSerializer

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


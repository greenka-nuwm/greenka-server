from django.contrib.auth.models import User, UserManager
from rest_framework import serializers

from tree import models
from gauth.models import Feedback, FeedbackImage


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('user_permissions', 'is_active', 'last_login', )
        depth = 1

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserGETSerializer(UserSerializer):

    class Meta:
        model = User
        exclude = ('password', 'user_permissions', 'is_active', 'last_login', )
        depth = 1


class FeedbackImageSerializer(serializers.ModelSerializer): 
    url = serializers.SerializerMethodField()

    class Meta:
        model = FeedbackImage
        fields = ('url', )

    def get_url(self, image):
        return '/' + str(image.url)


class FeedbackSerializer(serializers.ModelSerializer):
    images = FeedbackImageSerializer(many=True, read_only=True)

    class Meta:
        model = Feedback
        exclude = ('owner', 'is_active', )

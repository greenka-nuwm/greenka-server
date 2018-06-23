from django.contrib.auth.models import User, UserManager
from rest_framework import serializers

from tree import models
from gauth.models import Feedback


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


class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        exclude = ('owner', 'is_active', )
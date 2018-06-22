from django.contrib.auth.models import User, UserManager
from rest_framework import serializers

from tree import models


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
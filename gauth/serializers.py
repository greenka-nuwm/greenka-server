from django.contrib.auth.models import User, UserManager
from rest_framework import serializers

from tree import models


class UserSerializer(serializers.ModelSerializer):
    trees = serializers.PrimaryKeyRelatedField(many=True, required=False,
                                               queryset=models.Tree.objects.all())

    class Meta:
        model = User
        exclude = ('password', 'user_permissions', 'is_active', 'last_login', )
        depth = 1

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
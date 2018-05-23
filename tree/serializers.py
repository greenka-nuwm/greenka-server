from django.contrib.auth.models import User
from rest_framework import serializers
from tree.models import Tree, TreeType, TreeSort, TreeImages


class UserSerializer(serializers.ModelSerializer):
    trees = serializers.PrimaryKeyRelatedField(many=True,
                                               queryset=Tree.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'trees')
        depth = 1


class TreeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    distance = serializers.FloatField(read_only=True)

    class Meta:
        model = Tree
        fields = "__all__"

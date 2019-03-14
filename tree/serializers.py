import os
from django.contrib.auth.models import User
from rest_framework import serializers
from tree import models


class TreeImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = models.TreeImages
        fields = ('url', )

    def get_url(self, image):
        return '/' + str(image.url)


class TreeSortSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TreeSort
        fields = "__all__"


class TreeTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TreeType
        fields = "__all__"


class TreeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    approved = serializers.ReadOnlyField()
    visible = serializers.ReadOnlyField()
    distance = serializers.FloatField(read_only=True)
    images = TreeImageSerializer(many=True, read_only=True)
    confirms = serializers.SerializerMethodField()
    favourite_trees = None

    class Meta:
        model = models.Tree
        exclude = ('is_active', 'favourite_trees', )
        read_only = ('confirms', )

    def get_confirms(self, tree):
        return tree.confirms.all().count()

    def validate(self, data):
        """Check it tree sort is subtype of type"""
        sort = data.get('tree_sort')
        if not sort:
            return data

        tree_type = data.get('tree_type')
        if tree_type:
            if sort.tree_type != tree_type:
                raise serializers.ValidationError('Tree type must be the same as sort type ')
        else:
            data['tree_type'] = sort.tree_type
        return data


class TreeGETSerializer(TreeSerializer):
    """Overriding for GET request types."""
    tree_sort = TreeSortSerializer(read_only=True)
    tree_type = TreeTypeSerializer(read_only=True)
    favourite_trees = serializers.SerializerMethodField()

    def get_favourite_trees(self, tree):
        """Return if tree is user`s favourite"""
        if 'request' in self.context and self.context['request'].user:
            return tree.favourite_trees.filter(pk=self.context.get('request').user.pk).exists()
        return False


class TreeGETShortSerializer(TreeSerializer):

    class Meta:
        model = models.Tree
        fields = ('id', 'tree_state', 'latitude', 'longitude', 'distance', )

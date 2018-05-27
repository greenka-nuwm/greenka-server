import os
from django.contrib.auth.models import User
from rest_framework import serializers
from tree import models


class UserSerializer(serializers.ModelSerializer):
    trees = serializers.PrimaryKeyRelatedField(many=True,
                                               queryset=models.Tree.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'trees')
        depth = 1


class TreeImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = models.TreeImages
        fields = ('url', )

    def get_url(self, image):
        return os.sep + str(image.url)


class TreeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    distance = serializers.FloatField(read_only=True)
    images = TreeImageSerializer(many=True, read_only=True)
    confirms = serializers.SerializerMethodField()

    class Meta:
        model = models.Tree
        exclude = ('active', )
        read_only = (
            'confirms',
        )

    def get_confirms(self, tree):
        return tree.confirms.all().count()


class PolyPointSerializer(serializers.ModelSerializer):
    poly = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.PolyPoint
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        if 'as_nested' in kwargs:
            kwargs.pop('as_nested')
            self.fields.pop('poly')
        super(PolyPointSerializer, self).__init__(*args, **kwargs)


class PolygonSerializer(serializers.ModelSerializer):
    points = PolyPointSerializer(many=True, as_nested=True)

    class Meta:
        model = models.Polygon
        fields = "__all__"

    def create(self, validated_data):
        points = validated_data.pop('points')
        polygon = models.Polygon.objects.create(**validated_data)
        for point in points:
            models.PolyPoint.objects.create(poly=polygon, **point)
        return polygon
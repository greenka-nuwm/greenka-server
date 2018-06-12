from rest_framework import serializers

from polygon import models


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

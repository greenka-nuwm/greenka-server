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


class TreeImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = TreeImages
        fields = ('url', )

    def get_url(self, image):
        request = self.context.get('request')
        url = image.url.url
        return request.build_absolute_uri(url)


class TreeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    distance = serializers.FloatField(read_only=True)
    images = TreeImageSerializer(many=True, read_only=True)

    class Meta:
        model = Tree
        fields = "__all__"

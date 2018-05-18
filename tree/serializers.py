from rest_framework import serializers
from tree.models import Tree, TreeType, TreeSort, TreeImages


class TreeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tree
        fields = "__all__"
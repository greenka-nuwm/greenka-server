from rest_framework import serializers

from problems import models


class ProblemSerializer(serializers.ModelSerializer):
    confirms = serializers.SerializerMethodField()

    class Meta:
        model = models.Problem
        exclude = ("is_active", )
        read_only = (
            'creation_time',
            'modification_time',
            'confirms'
        )

    def get_confirms(self, problem):
        return problem.confirms.all().count()

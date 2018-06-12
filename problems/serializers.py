from uuid import uuid4
from rest_framework import serializers

from problems import models


class ProblemStateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProblemState
        exclude = ("is_active", )


class ProblemTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProblemType
        exclude = ('is_active', )


class ProblemPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProblemPhoto
        exclude = ('is_active', )


class ProblemSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField()
    problem_state = serializers.ReadOnlyField(source='problem_state.id')
    problem_state_name = serializers.ReadOnlyField(source='problem_state.verbose_name')
    reporter = serializers.ReadOnlyField(source='reporter.id')
    confirms = serializers.SerializerMethodField()
    photos = ProblemPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = models.Problem
        exclude = ("is_active", )
        read_only = (
            'creation_time',
            'modification_time',
            'confirms',
        )

    def get_confirms(self, problem):
        return problem.confirms.all().count()

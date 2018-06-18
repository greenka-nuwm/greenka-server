import os
from uuid import uuid4
from rest_framework import serializers

from problems import models


class ProblemStateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProblemState
        exclude = ("is_active", )

class ProblemStateShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProblemState
        exclude = ('is_active', 'description', 'id', )


class ProblemTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProblemType
        exclude = ('is_active', )


class ProblemTypeShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProblemType
        exclude = ('is_active', 'description', 'id', )


class ProblemImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = models.ProblemImage
        exclude = ('is_active', )

    def get_url(self, image):
        return os.sep + str(image.url)


class ProblemSerializer(serializers.ModelSerializer):
    problem_state = serializers.ReadOnlyField(source='problem_state.id')
    problem_state_name = serializers.ReadOnlyField(source='problem_state.verbose_name')
    reporter = serializers.ReadOnlyField(source='reporter.id')
    confirms = serializers.SerializerMethodField()
    images = ProblemImageSerializer(many=True, read_only=True)

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


class ProblemGETSerializer(ProblemSerializer):
    problem_state = ProblemStateShortSerializer(read_only=True)
    problem_type = ProblemTypeShortSerializer(read_only=True)


class ProblemGETShortSerializer(ProblemGETSerializer):

    class Meta:
        model = models.Problem
        fields = ('id', 'latitude', 'longitude', 'problem_type', 'problem_state', )

from rest_framework import serializers

from tree import models
from gauth.models import Feedback, FeedbackImage, User


class UserSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()
    profile_background_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ('user_permissions', 'is_active', 'last_login', )
        depth = 1

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def get_profile_image(self, user):
        if user.profile_image:
            return '/' + str(user.profile_image.url)
        return None

    def get_profile_background_image(self, user):
        if user.profile_background_image:
            return '/' + str(user.profile_background_image.url)
        return None


class UserEditSerializer(UserSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        depth = 1


class UserGETSerializer(UserSerializer):

    class Meta:
        model = User
        exclude = ('password', 'user_permissions', 'is_active', 'last_login', )
        depth = 1


class UserProfileImageSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('profile_image', )


class UserBackgroundImageSerializer(serializers.ModelSerializer):
    profile_background_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('profile_background_image', )


class FeedbackImageSerializer(serializers.ModelSerializer): 
    url = serializers.SerializerMethodField()

    class Meta:
        model = FeedbackImage
        fields = ('url', )

    def get_url(self, image):
        return '/' + str(image.url)


class FeedbackSerializer(serializers.ModelSerializer):
    images = FeedbackImageSerializer(many=True, read_only=True)

    class Meta:
        model = Feedback
        exclude = ('owner', 'is_active', )

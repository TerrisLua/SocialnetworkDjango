from rest_framework import serializers
from .models import *

# I wrote this code

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["name", "image"]


class ImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["name", "image"]


class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = [
            "user",
            "status_update",
            "organisation",
            "image",
            "thumbnail",
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


# end of code I wrote

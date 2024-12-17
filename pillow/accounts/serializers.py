from rest_framework import serializers

from . import models

class UserSigninSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        exclude = []
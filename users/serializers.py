from rest_framework import serializers

from users.models import UserModel


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ['id', 'email']
        extra_kwargs = {
            'id': {'read_only': True},
            'email': {'read_only': True},
        }


class AuthDataSerializer(serializers.Serializer):
    access_token = serializers.CharField(max_length=600)
    refresh_token = serializers.CharField(max_length=600)

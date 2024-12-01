from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

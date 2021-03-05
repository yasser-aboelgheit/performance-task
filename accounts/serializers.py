
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        exclude = ('is_superuser', 'is_staff')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class SuperUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ( ,'is_superuser', 'is_staff')

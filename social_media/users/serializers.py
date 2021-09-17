from django.db import models
from rest_framework import serializers
from users.models import User
from rest_framework.exceptions import ValidationError


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)


    class Meta:
        model = User
        fields = ['username','phone_number', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, **kwargs):
        user = User(
            username=self.validated_data['username'],
            phone_number=self.validated_data['phone_number'],
        )
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']
        if password != confirm_password:
            raise serializers.ValidationError({'password': 'Passwords must match'})
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(required=True, write_only=True)


    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'usrname': {"validators": []}}

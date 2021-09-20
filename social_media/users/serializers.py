import random

from django.core.cache import cache
from rest_framework import serializers
from users.models import User

from users.utils import send_verification_code

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

        phone_number = self.validated_data['phone_number']
        verify_code = random.randint(11111, 99999)

        cache_key = f'login_code_{phone_number}'
        cache.set(cache_key, verify_code, timeout=120)

        sent = send_verification_code(user, verify_code)

        if sent:
            user.save()
            return user
        else:
            raise serializers.ValidationError('Wrong verification code.try again')


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(required=True, write_only=True)


    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'usrname': {"validators": []}}


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError('Current password does not match')
        return value
        

    def validate_new_password(self, value):
        return value

    class Meta:
        model = User
        fields = ['current_password', 'new_password']

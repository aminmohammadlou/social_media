from django.core.cache import cache
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from users.tasks import send_verification_code_task
from social_media.settings import SIMPLE_JWT
from notifications.models import Notification
from .utils import email_generator

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def validate(self, attrs):
        password = attrs['password']
        confirm_password = attrs['confirm_password']
        if password != confirm_password:
            raise serializers.ValidationError({'password': 'Passwords dont match'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        email_data = email_generator(user.email)
        send_verification_code_task.apply_async((email_data,))
        return user


class VerifySerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)
    verification_code = serializers.IntegerField(min_value=10000, max_value=99999, required=True)

    class Meta:
        fields = ['email', 'verification_code']

    def validate(self, attrs):
        email = attrs['email']
        verification_code = attrs['verification_code']
        sent_code = cache.get(email, 'Code has expired')

        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise serializers.ValidationError({'email': 'Wrong email'})

        if not user.is_verified:
            if sent_code != verification_code:
                if sent_code == 'Code has expired':
                    email_data = email_generator(email)
                    send_verification_code_task.apply_async((email_data,))
                    raise serializers.ValidationError(
                        {'verification_code': 'code has expired.A new Verification code has been sent to your email'})

                raise serializers.ValidationError({'verification_code': 'Wrong code!Try again'})

            user.is_verified = True
            user.save()
            token = LoginSerializer.get_tokens_for_user(user)
            update_last_login(None, user)
            attrs['token'] = token

            return attrs

        else:
            raise serializers.ValidationError({'user': 'Your account is already verified'})


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs['email'])
        except ObjectDoesNotExist:
            raise serializers.ValidationError({'email': 'Wrong email'})

        user.is_verified = False
        user.set_unusable_password()
        user.save()
        email_data = email_generator(user.email)
        send_verification_code_task.apply_async((email_data,))
        return attrs


class SetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['password', 'confirm_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError('Passwords dont match')
        return attrs

    def update(self, instance, validated_data):
        if not instance.has_usable_password():
            instance.set_password(validated_data['password'])
            instance.save()
            return instance

        raise serializers.ValidationError({'password': 'You already set your password.call change password instead'})


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        fields = ['username', 'password']
        extra_kwargs = {'username': {"validators": []}}

    def validate(self, attrs):
        user = authenticate(**attrs)

        if not user:
            raise serializers.ValidationError(
                'Invalid username or password. Please try again!'
            )

        token = self.get_tokens_for_user(user)
        update_last_login(None, user)
        return token

    @staticmethod
    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'lifetime': int(SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()),
        }


class FollowSerializer(serializers.Serializer):
    following_user = serializers.CharField(max_length=100, required=True)

    def validate(self, attrs):
        follower = self.context.get('request').user
        try:
            following_user = User.objects.get(username=attrs['following_user'])
        except ObjectDoesNotExist:
            raise serializers.ValidationError('User with this username does not exist')

        if follower != following_user:
            if follower in following_user.followers.all():
                follower.following.remove(following_user)
                following_user.followers.remove(follower)
                message = 'User successfully unfollowed'

            else:
                follower.following.add(following_user)
                following_user.followers.add(follower)
                Notification.objects.create(from_user=follower, to_user=following_user,
                                            action=Notification.ACTION_CHOICES[1][0])
                message = 'User successfully followed'

            data = {
                'success': message,
                'follower': follower.username,
                'following_user': following_user.username,
            }
            return data

        raise serializers.ValidationError("You can't follow or unfollow yourself")

    class Meta:
        fields = ['following_user']


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if not self.context['request'].user.check_password(attrs['current_password']):
            raise serializers.ValidationError('Current password does not match')

        elif attrs['new_password'] != attrs['confirm_new_password']:
            raise serializers.ValidationError('New password and confirm new password dont match')

        elif attrs['current_password'] == attrs['new_password']:
            raise serializers.ValidationError('New password and current password are same')
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance

    class Meta:
        fields = ['current_password', 'new_password', 'confirm_new_password']


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()

    @staticmethod
    def get_full_name(user):
        return user.get_full_name()

    @staticmethod
    def get_posts_count(user):
        return user.post_set.all().count()

    @staticmethod
    def get_following_count(user):
        return user.following.all().count()

    @staticmethod
    def get_followers_count(user):
        return user.followers.all().count()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', 'phone_number', 'avatar', 'created_time', 'posts_count',
                  'following_count', 'followers_count']

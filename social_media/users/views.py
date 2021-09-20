from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import generics, status
from .serializers import RegistrationSerializer, LoginSerializer, ChangePasswordSerializer
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = {
                'success': 'Successfully Registered',
                'username': user.username,
            }
        
        return Response(data=data, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)

        if user is None:
            raise ValidationError('Invalid username/password. Please try again!')

        try:
            token = Token.objects.get(user_id=user.id)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)

        data = {
            'success': 'Successfully logged in',
            'username': user.username,
            'token': token.key
            
        }
        return Response(data=data, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        request.user.auth_token.delete()
        data = {'success': 'Successfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)


class FollowAPIView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        follower = request.user
        following_user = User.objects.get(username=request.data['following_user'])

        if follower != following_user:
            if follower in following_user.followers.all():
                follower.following.remove(following_user)
                following_user.followers.remove(follower)
                message = 'User successfully unfollewed'

            else:
                follower.following.add(following_user)
                following_user.followers.add(follower)
                message = 'User successfully follewed'

            data = {
                'success': message,
                'follower': follower.username,
                'follwing_user': following_user.username,
            }
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            raise ValidationError("You can't follow/unfollow yourself")


class ChangePasswordAPIVIEW(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data ,context={'request': request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        data = {
            'success': 'Password sccessfully changed'
        }
        return Response(data=data, status=status.HTTP_204_NO_CONTENT)

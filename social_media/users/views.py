from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .permissions import IsOwnerOrFollower, IsOwner
from .serializers import (RegistrationSerializer, ForgetPasswordSerializer, SetPasswordSerializer, LoginSerializer,
                          ChangePasswordSerializer, UserSerializer, UserMinSerializer, VerifySerializer,
                          FollowSerializer)

User = get_user_model()


class RegisterAPIView(APIView):
    serializer_class = RegistrationSerializer
    throttle_scope = 'users'

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = {
            'success': 'Verification code has been sent to your email',
            'email': user.email
        }

        return Response(data=data, status=status.HTTP_200_OK)


class VerifyAPIView(APIView):
    serializer_class = VerifySerializer
    throttle_scope = 'users'

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = {
            'success': 'Successfully verified',
            'token': serializer.validated_data['token']
        }
        return Response(data=data, status=status.HTTP_200_OK)


class ForgetPasswordAPIView(APIView):
    serializer_class = ForgetPasswordSerializer
    throttle_scope = 'users'

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = {
            'success': 'Verification code has been sent to your email',
            'email': request.data['email']
        }

        return Response(data=data, status=status.HTTP_200_OK)


class SetPasswordAPIView(generics.UpdateAPIView):
    serializer_class = SetPasswordSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_scope = 'users'

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'success': 'Password successfully set'
        }
        return Response(data=data, status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    throttle_scope = 'users'

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.validated_data, status=status.HTTP_200_OK)


class FollowAPIView(APIView):
    serializer_class = FollowSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_scope = 'users'

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.validated_data, status=status.HTTP_200_OK)


class ChangePasswordAPIVIEW(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_scope = 'users'

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'success': 'Password successfully changed'
        }
        return Response(data=data, status=status.HTTP_200_OK)


class FollowingListAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrFollower]
    serializer_class = UserSerializer
    throttle_scope = 'users'

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        followings = user.following.all()
        serializer = self.serializer_class(followings, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class FollowerListAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrFollower]
    serializer_class = UserSerializer
    throttle_scope = 'users'

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        followers = user.followers.all()
        serializer = self.serializer_class(followers, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserDetailAPIView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'


class PostLikeListAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserMinSerializer

    def get_queryset(self):
        return User.objects.filter(likes_post=self.request.query_params['post_id'])


class UserSearchAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserMinSerializer
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'first_name', 'last_name']

    def get_queryset(self):
        if self.request.query_params.get('search'):
            return self.queryset
        return User.objects.none()


class UserUpdateAPIView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwner]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_update(self, serializer):
        if self.request.data.get('first_name') or self.request.data.get('last_name'):
            serializer.Meta.fields.append('first_name')
            serializer.Meta.fields.append('last_name')
            serializer.Meta.extra_kwargs = {'first_name': {'write_only': True},
                                            'last_name': {'write_only': True}}

        return super(UserUpdateAPIView, self).perform_update(serializer)

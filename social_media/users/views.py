from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import generics, status
from .serializers import RegistrationSerializer, LoginSerializer
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


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

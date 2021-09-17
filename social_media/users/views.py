from rest_framework.response import Response
from rest_framework import generics, status
from .serializers import RegistrationSerializer
from rest_framework import permissions
from .models import User


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

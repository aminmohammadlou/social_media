from rest_framework import generics, filters
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Notification
from .serializers import NotificationSerializer


class NotificationListAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ['-created_time']

    def get_queryset(self):
        return Notification.objects.filter(to_user=self.request.user)

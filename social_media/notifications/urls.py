from django.urls import path

from .views import (NotificationListAPIView)

app_name = 'notifications'

urlpatterns = [
    path('list/', NotificationListAPIView.as_view(), name='list')
]

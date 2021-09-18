from django.urls import path
from .views import PublishAPIView

app_name = 'posts'

urlpatterns = [
    path('publish', PublishAPIView.as_view(), name='publish'),
]
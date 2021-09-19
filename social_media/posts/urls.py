from django.urls import path
from .views import PublishAPIView, LikeAPIView, CommentAPIView

app_name = 'posts'

urlpatterns = [
    path('publish', PublishAPIView.as_view(), name='publish'),
    path('like', LikeAPIView.as_view(), name='like'),
    path('comment', CommentAPIView.as_view(), name='comment'),
]
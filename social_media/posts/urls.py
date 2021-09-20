from django.urls import path
from .views import PublishAPIView, LikeAPIView, CommentAPIView, PostListAPIView, PostDetailAPIView, DeletePostAPIVIew

app_name = 'posts'

urlpatterns = [
    path('publish/', PublishAPIView.as_view(), name='publish'),
    path('like/<int:pk>', LikeAPIView.as_view(), name='like'),
    path('comment/<int:pk>', CommentAPIView.as_view(), name='comment'),
    path('posts-list/', PostListAPIView.as_view(),name='posts_list'),
    path('post-detail/<int:pk>/', PostDetailAPIView.as_view(), name='post_detail'),
    path('delete/<int:pk>/', DeletePostAPIVIew.as_view(), name='delete'),
]
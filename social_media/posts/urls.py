from django.urls import path

from rest_framework import routers

from .views import PostViewSet, CommentViewSet, SearchPostAPIView, UserTagedPostAPIView

app_name = 'posts'

router = routers.SimpleRouter()
router.register(r'post', PostViewSet)
router.register(r'comment', CommentViewSet)
urlpatterns = [
    path('post/search/', SearchPostAPIView.as_view(), name='search_hashtag'),
    path('post/taged/', UserTagedPostAPIView.as_view(), name='user_taged_posts'),
              ] + router.urls

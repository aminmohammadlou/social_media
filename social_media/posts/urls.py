from django.urls import path

from rest_framework import routers

from .views import PostViewSet, CommentViewSet, SearchHashtagAPIView

app_name = 'posts'

router = routers.SimpleRouter()
router.register(r'post', PostViewSet)
router.register(r'comment', CommentViewSet)
urlpatterns = [
    path('hashtag/search/', SearchHashtagAPIView.as_view(), name='search_hashtag')
              ] + router.urls

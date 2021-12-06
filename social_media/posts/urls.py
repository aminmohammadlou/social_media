from rest_framework import routers

from .views import PostViewSet, CommentViewSet

app_name = 'posts'

router = routers.SimpleRouter()
router.register(r'post', PostViewSet)
router.register(r'comment', CommentViewSet)
urlpatterns = router.urls

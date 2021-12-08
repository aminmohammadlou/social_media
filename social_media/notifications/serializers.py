from rest_framework import serializers

from users.serializers import UserSerializer
from posts.serializers import PostSerializer, CommentSerializer
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    action = serializers.CharField(source='get_action_display')
    from_user = UserSerializer()
    post = PostSerializer()
    comment = CommentSerializer()
    to_user = UserSerializer()

    class Meta:
        model = Notification
        fields = ['action', 'from_user', 'post', 'comment', 'to_user', 'created_time']

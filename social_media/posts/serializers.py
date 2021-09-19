from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True)
    class Meta:
        model = Post
        fields = ['caption', 'image', 'location']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['message', 'created_time']

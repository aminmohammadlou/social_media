from rest_framework import serializers
from .models import Post, Comment


class PublishPostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True)
    class Meta:
        model = Post
        fields = ['id', 'caption', 'image', 'location', 'created_time']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'caption', 'created_time']


class PostDetailSerilaizer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(default=0)
    comments_count = serializers.IntegerField(default=0)

    class Meta:
        model = Post
        fields = ['id', 'author', 'caption', 'image',
        'location', 'created_time', 'likes_count', 'comments_count']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['message', 'created_time']

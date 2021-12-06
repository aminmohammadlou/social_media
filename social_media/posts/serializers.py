from django.contrib.auth import get_user_model

from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Post, Comment

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author_detail = UserSerializer(source='author', read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['author']

    @staticmethod
    def get_likes_count(post):
        return post.likes.all().count()

    @staticmethod
    def get_comments_count(post):
        return post.comment_set.count()


class CommentSerializer(serializers.ModelSerializer):
    author_detail = UserSerializer(source='author', read_only=True)
    post_detail = PostSerializer(source='post', read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['author']

    @staticmethod
    def get_likes_count(comment):
        return comment.likes.all().count()

    @staticmethod
    def get_comments_count(comment):
        return comment.comments.all().count()

from rest_framework import serializers
from .models import Post, Comment


class PublishPostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True)
    class Meta:
        model = Post
        fields = ['id', 'caption', 'image', 'location', 'created_time']


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_username_from_author')

    class Meta:
        model = Post
        fields = ['id', 'author', 'caption', 'created_time']

    def get_username_from_author(self, post):
        author = post.author.username
        return author


class PostDetailSerilaizer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(default=0)
    comments_count = serializers.IntegerField(default=0)
    author = serializers.SerializerMethodField('get_username_from_author')

    class Meta:
        model = Post
        fields = ['id', 'author', 'caption', 'image',
        'location', 'created_time', 'likes_count', 'comments_count']

    def get_username_from_author(self, post):
        author = post.author.username
        return author

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['message', 'created_time']

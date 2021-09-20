from rest_framework import serializers
from .models import Post, Comment


class PublishPostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True)
    class Meta:
        model = Post
        fields = ['id', 'caption', 'image', 'location', 'created_time']


class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField('get_post_likes')
    comments_count = serializers.SerializerMethodField('get_post_comments')
    author = serializers.SerializerMethodField('get_username_from_author')

    class Meta:
        model = Post
        fields = ['id', 'author', 'caption', 'image',
        'location', 'created_time', 'likes_count', 'comments_count']

    def get_username_from_author(self, post):
        author = post.author.username
        return author

    def get_post_likes(self, post):
        likes_count = post.likes.all().count()
        return likes_count

    def get_post_comments(self, post):
        comments_count = Comment.objects.filter(post_id=post.id).count()
        return comments_count


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['message', 'created_time']

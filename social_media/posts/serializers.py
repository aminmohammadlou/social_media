from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True)
    class Meta:
        model = Post
        fields = ['caption', 'image', 'location']

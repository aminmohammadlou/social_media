from re import A
from django.contrib import auth
from rest_framework.exceptions import ValidationError
from .models import Post
from rest_framework.response import Response
from rest_framework import generics, serializers, status
from .serializers import PostSerializer
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


class PublishAPIView(generics.GenericAPIView):
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        # serializer = self.serializer_class(data=request.data)
        # post = serializer.save()
        # post.author = request.user
        author = request.user
        post = Post(author=author)
        serializer = PostSerializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
                'success': 'Post successfully created ',
                'post': {
                    'caption': post.caption,
                    'author': post.author.username,
                    'location': post.location,
                    'created_time': post.created_time
                }
            }
        
        return Response(data=data, status=status.HTTP_201_CREATED)

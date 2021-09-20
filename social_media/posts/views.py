from django.http.response import Http404
from .models import Post, Comment
from rest_framework.response import Response
from rest_framework import generics, status
from .serializers import PostSerializer, CommentSerializer, PublishPostSerializer
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError


class PublishAPIView(generics.GenericAPIView):
    serializer_class = PublishPostSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        author = request.user
        post = Post(author=author)
        serializer = self.serializer_class(post, data=request.data)
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


class LikeAPIView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def post(self, request, pk):
        post = self.get_object(pk)
        author = request.user

        if author in post.likes.all():
            post.likes.remove(author)
            message = 'Post successfully unliked'
            stat = status.HTTP_204_NO_CONTENT
        else:
            post.likes.add(author)
            message = 'Post successfully liked'
            stat = status.HTTP_201_CREATED

        data = {
            'success': message,
            'author': author.username,
            'post_id': post.id
        }
        return Response(data=data, status=stat)


class CommentAPIView(generics.GenericAPIView):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def post(self, request, pk):
        author = request.user
        post = self.get_object(pk)
        comment = Comment(author=author, post=post)
        serializer = self.serializer_class(comment, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
                'success': 'Comment successfully added ',
                'comment': {
                    'message': comment.message,
                    'author': comment.author.username,
                    'post': comment.post.pk,
                    'created_time': comment.created_time
                }
            }
        
        return Response(data=data, status=status.HTTP_201_CREATED)


class PostListAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated, )
    pagination_class = PageNumberPagination

class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'


class DeletePostAPIVIew(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        if request.user != post.author:
            raise ValidationError('You dont have permission to delete this post')
        post.delete()
        data = {
            'success': 'Post successfully deleted'
        }
        return Response(data=data, status=status.HTTP_204_NO_CONTENT)


class DeleteCommentAPIView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        comment = self.get_object(pk)
        if request.user != comment.author:
            raise ValidationError('You dont have permission to delete this comment')
        comment.delete()
        data = {
            'success': 'Comment successfully deleted'
        }
        return Response(data=data, status=status.HTTP_204_NO_CONTENT)

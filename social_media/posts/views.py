from .models import Post, Comment
from rest_framework.response import Response
from rest_framework import generics, status
from .serializers import PostSerializer, CommentSerializer
from rest_framework import permissions


class PublishAPIView(generics.GenericAPIView):
    serializer_class = PostSerializer
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

    def post(self, request):
        post_id = request.data['post_id']
        post = Post.objects.get(pk=post_id)
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
            'post_id': post_id
        }
        return Response(data=data, status=stat)


class CommentAPIView(generics.GenericAPIView):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        author = request.user
        post = Post.objects.get(pk=request.data['post_id'])
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

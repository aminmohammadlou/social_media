from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from notifications.models import Notification

from .models import Post, Comment
from .permissions import get_post_access_list, get_comment_access_list
from .serializers import PostSerializer, CommentSerializer

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_scope = 'posts'
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['author_id']
    ordering = ['pk']

    def get_queryset(self):
        if self.action == 'home_page':
            return self.queryset.filter(Q(author=self.request.user) | Q(author__in=self.request.user.following.all()))

        if self.action == 'feed':
            return self.queryset.filter(
                Q(likes__in=self.request.user.following.all()) | Q(
                    likes__in=self.request.user.followers.all())).exclude(
                author=self.request.user).distinct()

        return self.queryset

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        if self.request.data.get('taged_users'):
            for taged_user in self.request.data.pop('taged_users'):
                Notification.objects.create(from_user=self.request.user, post=post, to_user_id=int(taged_user),
                                            action=Notification.ACTION_CHOICES[2][0])

    def perform_update(self, serializer):
        super(PostViewSet, self).perform_update(serializer)
        post = self.get_object()
        if self.request.data.get('taged_users'):
            for taged_user in serializer['taged_users'].value:
                Notification.objects.get_or_create(from_user=self.request.user, post=post, to_user_id=int(taged_user),
                                                   action=Notification.ACTION_CHOICES[2][0])

    @action(methods=['post'], detail=True)
    def like(self, request, *args, **kwargs):
        user = request.user
        post = self.get_object()
        if user in post.likes.all():
            post.likes.remove(user)

            message = 'Post successfully unliked'
        else:
            post.likes.add(user)
            Notification.objects.create(from_user=user, post=post, action=Notification.ACTION_CHOICES[0][0])
            message = 'Post successfully liked'
        return Response(data={'post_id': post.id, 'message': message}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def home_page(self, request, *args, **kwargs):
        self.ordering = ['-created_time']
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def feed(self, request, *args, **kwargs):
        self.ordering = ['-created_time']
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_scope = 'comments'
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_queryset(self):
        if self.request.method == 'GET' and self.request.query_params.get('post_id'):
            return self.queryset.filter(post_id=self.request.query_params['post_id'])

        access_list = get_comment_access_list(self.request.user)
        return self.queryset.filter(pk__in=access_list)

    def perform_create(self, serializer):
        if self.request.data.get('post') is None and self.request.data.get('parent') is None:
            raise ValidationError({'error': 'Post or parent is required'})

        if self.request.data.get('post') and self.request.data.get('parent'):
            raise ValidationError({'error': 'One of these two fields is required: post or parent'})

        if self.request.data.get('post') is None:
            post = Comment.objects.get(pk=self.request.data['parent']).post
            serializer.save(author=self.request.user, post=post)

        else:
            serializer.save(author=self.request.user)

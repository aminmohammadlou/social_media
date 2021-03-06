from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from rest_framework import status, viewsets, filters, generics
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from notifications.models import Notification

from .models import Post, SavedPost, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwner

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_scope = 'posts'
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['author_id']
    ordering = ['-created_time']

    def get_queryset(self):
        filter_params = {
            'list': {'is_archive': False},
            'collection': {'savedpost__user': self.request.user},
            'archived': {'author': self.request.user,
                         'is_archive': True}
        }.get(self.action, dict())

        if self.action == 'home_page':
            return self.queryset.filter(Q(author=self.request.user) | Q(author__in=self.request.user.following.all()),
                                        is_archive=False)

        if self.action == 'feed':
            return self.queryset.filter(
                Q(likes__in=self.request.user.following.all()) | Q(
                    comment__author__in=self.request.user.following.all()), is_archive=False).exclude(
                author=self.request.user).distinct()

        if self.action == 'list' and not self.request.query_params.get('author_id'):
            return Post.objects.none()

        return self.queryset.filter(**filter_params)

    def get_permissions(self):
        actions = ['partial_update', 'update', 'destroy']
        if self.action in actions:
            return [IsOwner()]

        return super(PostViewSet, self).get_permissions()

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        if self.request.data.get('taged_users'):
            for taged_user in self.request.data.pop('taged_users'):
                Notification.objects.create(from_user=self.request.user, post=post, to_user_id=int(taged_user),
                                            action=Notification.ACTION_CHOICES[2][0])

    def perform_update(self, serializer):
        taged_users = list(self.get_object().taged_users.all().values_list('pk', flat=True))
        super(PostViewSet, self).perform_update(serializer)
        post = self.get_object()
        if self.request.data.get('taged_users'):
            for taged_user_id in taged_users:
                if taged_user_id not in serializer['taged_users'].value:
                    Notification.objects.get(from_user=self.request.user, post=post, to_user_id=taged_user_id,
                                             action=Notification.ACTION_CHOICES[2][0]).delete()

            for taged_user_id in serializer['taged_users'].value:
                Notification.objects.get_or_create(from_user=self.request.user, post=post,
                                                   to_user_id=int(taged_user_id),
                                                   action=Notification.ACTION_CHOICES[2][0])

    def perform_destroy(self, instance):
        instance.image.delete()
        super(PostViewSet, self).perform_destroy(instance)

    @action(methods=['post'], detail=True)
    def like(self, request, *args, **kwargs):
        user = request.user
        post = self.get_object()
        if user in post.likes.all():
            post.likes.remove(user)

            message = 'Post successfully unliked'
        else:
            post.likes.add(user)
            Notification.objects.update_or_create(from_user=user, post=post, to_user=post.author,
                                                  action=Notification.ACTION_CHOICES[0][0])
            message = 'Post successfully liked'
        return Response(data={'post_id': post.id, 'message': message}, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def collect(self, request, *args, **kwargs):
        post = self.get_object()
        if post.is_archive is True:
            raise ValidationError({'message': 'Post is archived! You cant add it to your collection',
                                   'code': 400})
        user = self.request.user
        try:
            SavedPost.objects.get(post=post, user=user).delete()
            data = {
                'message': 'Post successfully removed from your collection',
                'code': 200
            }
        except ObjectDoesNotExist:
            SavedPost.objects.create(post=post, user=user)
            data = {
                'message': 'Post successfully added to your collection',
                'code': 200
            }
        return Response(data=data)

    @action(methods=['get'], detail=False)
    def home_page(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(methods=['get'], detail=False)
    def feed(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(methods=['get'], detail=False)
    def collection(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(methods=['get'], detail=False)
    def archived(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_scope = 'comments'
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['post_id']
    ordering = ['created_time']

    def perform_create(self, serializer):
        if self.request.data.get('post') is None and self.request.data.get('parent') is None:
            raise ValidationError({'error': 'Post or parent is required'})

        if self.request.data.get('post') and self.request.data.get('parent'):
            raise ValidationError({'error': 'One of these two fields is required: post or parent'})

        if self.request.data.get('post') is None:
            comment = Comment.objects.get(pk=self.request.data['parent'])
            serializer.save(author=self.request.user, post=comment.post)
            Notification.objects.create(from_user=self.request.user, comment=comment, to_user=comment.author,
                                        action=Notification.ACTION_CHOICES[3][0])

        else:
            comment = serializer.save(author=self.request.user)
            Notification.objects.create(from_user=self.request.user, post=comment.post, to_user=comment.post.author,
                                        action=Notification.ACTION_CHOICES[3][0])

    @action(methods=['post'], detail=True)
    def like(self, request, *args, **kwargs):
        user = request.user
        comment = self.get_object()
        if user in comment.likes.all():
            comment.likes.remove(user)

            message = 'Comment successfully unliked'
        else:
            comment.likes.add(user)
            Notification.objects.update_or_create(from_user=user, comment=comment, to_user=comment.author,
                                                  action=Notification.ACTION_CHOICES[0][0])
            message = 'Comment successfully liked'
        return Response(data={'comment_id': comment.id, 'message': message}, status=status.HTTP_200_OK)


class SearchPostAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(is_archive=False)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['=caption', '=comment__message']
    ordering = ['-created_time']

    def get_queryset(self):
        if self.request.query_params.get('search'):
            if self.request.query_params.get('search').find('#') == -1:
                self.search_fields = ['location']

            return self.queryset
        return Post.objects.none()


class UserTagedPostAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(taged_users=self.kwargs['pk'], is_archive=False).order_by('-created_time')

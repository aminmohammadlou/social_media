from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.permissions import BasePermission, IsAuthenticated

User = get_user_model()


class IsOwnerOrFollower(BasePermission):
    def has_permission(self, request, view):
        owner = get_object_or_404(User, pk=view.kwargs['pk'])
        return bool(
            request.user and request.user.is_authenticated and (
                    request.user.pk == view.kwargs['pk']) or request.user in owner.followers.all())


class IsOwner(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj == request.user

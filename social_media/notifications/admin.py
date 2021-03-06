from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_user', 'post', 'comment', 'to_user', 'action', 'created_time', 'updated_time')
    ordering = ['-created_time']
    search_fields = ['from_user__username', 'to_user__username']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

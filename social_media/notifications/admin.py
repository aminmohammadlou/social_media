from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_user', 'post', 'comment', 'to_user', 'action', 'created_time', 'updated_time')
    ordering = ['-created_time']
    search_fields = ['from_user', 'post', 'to_user', 'action']
    raw_id_fields = ['from_user', 'post', 'to_user']

from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'email', 'phone_number', 'is_active', 'is_verified', 'is_staff', 'created_time',
        'updated_time')

    search_fields = ['username', 'email', 'phone_number']
    list_filter = ['is_active', 'is_verified', 'is_staff', 'gender']
    ordering = ['created_time']
    readonly_fields = ['password']
    raw_id_fields = ['followers', 'following']

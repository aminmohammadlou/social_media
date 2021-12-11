from django.contrib import admin

from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'caption', 'author', 'location', 'created_time', 'updated_time', 'image', 'is_archive')

    ordering = ['created_time']
    search_fields = ['author__username', 'location']
    list_filter = ['is_archive']
    raw_id_fields = ['taged_users', 'likes']
    

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'author', 'post', 'parent', 'created_time', 'updated_time')

    ordering = ['created_time']
    search_fields = ['author__username', 'post__id', 'parent__id']
    raw_id_fields = ['likes']

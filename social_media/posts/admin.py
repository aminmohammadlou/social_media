from django.contrib import admin
from .models import Post, Like, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'caption', 'author', 'location', 'likes_count', 'comments_count',
                    'created_time', 'updated_time')

    ordering = ('created_time',)
    

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'author', 'post', 'created_time', 'updated_time')

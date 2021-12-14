from django.contrib import admin

from .models import Post, SavedPost, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'location', 'created_time', 'updated_time', 'is_archive', 'image')

    ordering = ['created_time']
    search_fields = ['author__username', 'location']
    list_filter = ['is_archive']
    raw_id_fields = ['taged_users', 'likes']


@admin.register(SavedPost)
class SavedPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user')

    ordering = ['created_time']
    search_fields = ['user__username', 'post__id']
    raw_id_fields = ['post', 'user']
    

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post', 'parent', 'created_time', 'updated_time')

    ordering = ['created_time']
    search_fields = ['author__username', 'post__id', 'parent__id']
    raw_id_fields = ['likes']

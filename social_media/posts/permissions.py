from .models import Post, Comment


def get_post_access_list(user):
    return Post.objects.filter(author=user).values_list('pk', flat=True)


def get_comment_access_list(user):
    return Comment.objects.filter(author=user).values_list('pk', flat=True)

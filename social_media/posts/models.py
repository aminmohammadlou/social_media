from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Post(models.Model):
    caption = models.TextField(_('Caption'), max_length=500, blank=True, null=False)
    image = models.ImageField(_('Image'), upload_to='post_images', blank=False, editable=False)
    author = models.ForeignKey(User, verbose_name=_('Author'), on_delete=models.CASCADE)
    location = models.CharField(_('Location'), max_length=30, blank=True)
    likes = models.ManyToManyField(User, verbose_name=_('Likes'), related_name='likers', blank=True, symmetrical=False)
    likes_count = models.IntegerField(_('Likes Count'), default=0, blank=False, null=False)
    comments_count = models.IntegerField(_('Comments Count'), default=0, blank=False, null=False)
    created_time = models.DateTimeField(_('Created Time'), auto_now_add=True) 
    updated_time = models.DateTimeField(_('Updated Time'), auto_now=True)

    class Meta:
        db_table = 'post'
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def __str__(self):
        return f"{self.caption} by {self.author}"


class Like(models.Model):
    author = models.ForeignKey(User, verbose_name=_('Author'), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name=_('Post'), on_delete=models.CASCADE)

    class Meta:
        db_table = 'like'
        verbose_name = _('Like')
        verbose_name_plural = _('Likes')

    def __str__(self):
        return f"Like from {self.author} to {self.post}"


class Comment(models.Model):
    author = models.ForeignKey(User, verbose_name=_('Author'), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name=_('Post'), on_delete=models.CASCADE)
    message = models.TextField(_('Message'), max_length=500, blank=False, null=False)
    created_time = models.DateTimeField(_('Created Time'), auto_now_add=True) 
    updated_time = models.DateTimeField(_('Updated Time'), auto_now=True)
    
    class Meta:
        db_table = 'comment'
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def __str__(self):
        return f"Comment from {self.author} on {self.post}"
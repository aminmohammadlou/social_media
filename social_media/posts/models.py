from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models

from common.models import BaseModel

User = get_user_model()


class Post(BaseModel):
    image = models.ImageField(_('image'), upload_to='post_images')
    caption = models.TextField(_('caption'), max_length=500, blank=True)
    author = models.ForeignKey(User, verbose_name=_('author'), on_delete=models.PROTECT)
    taged_users = models.ManyToManyField(User, verbose_name=_('taged users'), blank=True,
                                         related_name='taged_users')
    location = models.CharField(_('location'), max_length=30, blank=True, null=True)
    likes = models.ManyToManyField(User, verbose_name=_('likes'), blank=True, related_name="likes_post")
    is_archive = models.BooleanField(_('is archive'), default=False)

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')

    def __str__(self):
        return 'id: {}'.format(self.pk)


class SavedPost(BaseModel):
    post = models.ForeignKey(Post, verbose_name=_('post'), on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=_('user'), on_delete=models.PROTECT)

    class Meta:
        verbose_name = _('saved post')
        verbose_name_plural = _('saved posts')


class Comment(BaseModel):
    author = models.ForeignKey(User, verbose_name=_('author'), on_delete=models.PROTECT)
    post = models.ForeignKey(Post, verbose_name=_('post'), on_delete=models.CASCADE, blank=True, null=True)
    message = models.TextField(_('message'), max_length=500)
    likes = models.ManyToManyField(User, verbose_name=_('likes'), related_name="comment_likers", blank=True)
    parent = models.ForeignKey('self', verbose_name=_('parent'), blank=True, null=True, related_name='comments',
                               on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    def __str__(self):
        return 'id: {}'.format(self.pk)

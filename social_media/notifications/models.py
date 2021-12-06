from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel
from posts.models import Post

User = get_user_model()


class Notification(BaseModel):
    LIKE = 1
    FOLLOW = 2
    TAG = 3
    COMMENT = 4

    from_user = models.ForeignKey(User, verbose_name=_('from_user'), on_delete=models.PROTECT, related_name='from_user')
    post = models.ForeignKey(Post, verbose_name=_('post'), blank=True, null=True, on_delete=models.PROTECT)
    to_user = models.ForeignKey(User, verbose_name=_('to_user'), blank=True, null=True, on_delete=models.PROTECT,
                                related_name='to_user')
    ACTION_CHOICES = (
        (LIKE, _('Like')),
        (FOLLOW, _('Follow')),
        (TAG, _('Tag')),
        (COMMENT, _('Comment')),
    )
    action = models.SmallIntegerField(_('action'), choices=ACTION_CHOICES)

    class Meta:
        verbose_name = _('notification')
        verbose_name_plural = _('notifications')

    def __str__(self):
        return self.get_action_display()

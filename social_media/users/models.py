from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.conf import settings

from common.models import BaseModel


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_verified = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    MALE = 0
    FEMALE = 1
    CUSTOM = 2

    username = models.CharField(_('username'), max_length=100, unique=True, db_index=True,
                                validators=[ASCIIUsernameValidator()])

    email = models.EmailField(_('email'), max_length=255, unique=True, db_index=True)

    phone_number_validator = RegexValidator(r'^(\+98|0)?9\d{9}$', message=_('Invalid phone number'))

    phone_number = models.PositiveBigIntegerField(_('phone number'), unique=True, db_index=True,
                                                  blank=True, null=True, validators=[phone_number_validator])

    is_verified = models.BooleanField(_('is verified'), default=False)
    is_active = models.BooleanField(_('is active'), default=True)
    is_staff = models.BooleanField(_('is staff'), default=False)

    first_name = models.CharField(_('first name'), max_length=100, blank=True)
    last_name = models.CharField(_('last name'), max_length=100, blank=True)

    GENDER_CHOICES = (
        (MALE, _('Male')),
        (FEMALE, _('Female')),
        (CUSTOM, _('Custom'))
    )
    gender = models.SmallIntegerField(_('gender'), choices=GENDER_CHOICES, blank=True, null=True)
    birthday = models.DateField(_('birthday'), blank=True, null=True)
    avatar = models.ImageField(_('avatar'), blank=True)

    bio = models.TextField(_('bio'), blank=True)
    other_social_medias = models.JSONField(verbose_name=_('other social medias'), blank=True, default=dict)

    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user followers'),
        related_name="Followers",
        blank=True,
        symmetrical=False
    )
    following = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user following'),
        related_name="Following",
        blank=True,
        symmetrical=False
    )
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def str(self):
        return self.username

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '{} {}'.format(self.first_name, self.last_name)
        return full_name.strip()

from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, username, phone_number, password=None):
        if username is None:
            raise TypeError(_('Username is a required field'))

        user = self.model(username=username, phone_number=phone_number)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, phone_number, password=None):
        if password is None:
            raise TypeError(_('Password is a required field'))

        user = self.create_user(username, phone_number, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_verified = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=100, unique=True)
    email = models.EmailField(_('email'), max_length=255, unique=True, blank=True, default=None, null=True)

    phone_number_validator = RegexValidator(r'^(\+98|0)?9\d{9}$', message=_('Invalid phone number'))

    phone_number = models.PositiveBigIntegerField(_('phone number'), unique=True, validators=[phone_number_validator])
    is_verified = models.BooleanField(_('is verified'), default=False)
    is_active = models.BooleanField(_('is active'), default=True)
    is_staff = models.BooleanField(_('is staff'), default=False)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number']

    objects = UserManager()

    def str(self):
        return self.username

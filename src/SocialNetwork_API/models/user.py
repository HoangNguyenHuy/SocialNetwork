from __future__ import unicode_literals
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin,
    BaseUserManager
)
from django.contrib.auth.signals import user_logged_in
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core import validators

from SocialNetwork_API.const import UserType, SexType
from SocialNetwork_API.models.user_types import TinyIntegerField


def update_last_login(sender, user, **kwargs):
    user.last_login = timezone.now()
    user.save(update_fields=['last_login'])


user_logged_in.connect(update_last_login)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_user', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _('username'),
        unique=True,
        max_length=20,
        default='',
        help_text=_('Required. 20 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                _('Enter a valid username. This value may contain only '
                  'letters, numbers ' 'and @/./+/-/_ characters.')
            ),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        _('email address'),
        unique=True,
        help_text=_('245 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _('A user with that email already exists.'),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class User(AbstractUser):
    is_disabled = models.BooleanField(default=False)
    manager_id = models.PositiveIntegerField(default=0)
    user_type = TinyIntegerField(default=UserType.USER)

    Sex=models.IntegerField(default=SexType.UNKNOWN)
    Phone = models.CharField(max_length=255, default="")
    MemoryUsed = models.FloatField(default=0)
    TotalMemory = models.FloatField(default=10)
    # DOB=???

    class Meta(AbstractUser.Meta):
        db_table = 'auth_user'
        swappable = 'AUTH_USER_MODEL'

    # @property
    # def is_band_admin(self):
    #     if self.user_type and self.user_type == UserType.USER:
    #         return True
    #     return False

    def __str__(self):
        return '{},type:{},mid:{}'.format(
            self.username,
            self.user_type,
            self.manager_id
        )

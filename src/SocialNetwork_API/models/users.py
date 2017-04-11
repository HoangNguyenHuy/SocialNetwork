# from django.utils import timezone
# from django.contrib.auth.signals import user_logged_in
# from django.contrib.auth.models import (
#     AbstractBaseUser, PermissionsMixin,
#     BaseUserManager
# )
#
#
# def update_last_login(sender, user, **kwargs):
#     user.last_login = timezone.now()
#     user.save(update_fields=['last_login'])
#
#
# user_logged_in.connect(update_last_login)
#
# class User
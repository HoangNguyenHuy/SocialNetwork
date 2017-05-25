import _thread
import time
import hashlib

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from django.conf import settings
from django.template.defaultfilters import slugify

from SocialNetwork_API.services.base import BaseService
from SocialNetwork_API.models import *
from SocialNetwork_API.const import ResourceType


class UserService(BaseService):

    @classmethod
    def get_all_users(cls):
        try:
            users = User.objects.all()
            if len(users) > 0:
                return users
            return None
        except Exception as exception:
            cls.log_exception(exception)
            return None

    @classmethod
    def get_user_friend(cls, user_id, friend_id):
        try:
            user_friend = Friend.objects.filter(user_id=user_id, friend_user_id=friend_id)
            if len(user_friend) > 0:
                return user_friend[0]
            return None
        except Exception as exception:
            cls.log_exception(exception)
            return None

    @classmethod
    def get_single_user(cls, user_id):
        try:
            return User.objects.get(pk=user_id)
        except:
            return None

    @classmethod
    def authenticate(cls, email, username, password):
        try:
            if email:
                user = User.objects.filter(email=email)[0]
            if username:
                user = User.objects.filter(username=username)[0]
            if user and user.check_password(password):
                return user
            else:
                return None
        except Exception as exception:
            return None

    @classmethod
    def save(cls, user_data, instance=None):
        try:
            password = user_data.data.pop('password', None)
            email = user_data.get('email', None)
            bands = user_data.pop('bands', None)

            user = instance if instance else User()
            is_new = instance is None

            current_email = user.email

            # Set property values
            if 'username' in user_data and user.username != user_data['username']:
                user.slug = slugify(user_data['username'])

            for key in user_data:
                setattr(user, key, user_data[key])

            # Set password
            if is_new:
                if not password and not user.password:
                    password = Utils.id_generator(8)
                user.set_password(password)
            else:
                if password:
                    user.set_password(password)

            with transaction.atomic():
                user.save()

                cls.save_relation_data(user, profile_data, band_data, fan_data, is_new)

                if email != current_email:
                    cls.add_email(user.id, user.email, current_email=current_email, is_primary=True, password=password,
                                  show_verify_link=True)

            # Follow users
            if is_new and bands and len(bands) > 0:
                cls.follow_bands(user, bands)

            if not is_new:
                # Reset cache
                cache_service = cls._get_cache_service()
                cache_service.delete(user.id)

            return cls.get_user(user.id)
        except Exception as exception:
            raise exception

    @classmethod
    def user_friend(cls, user, friend):
        try:
            user_friend = Friend()
            user_friend.user_id = user.id
            user_friend.follow_user_id = friend.id
            with transaction.atomic():
                # Save follow_user to mysqldb
                user_friend.save()

                # # Save follow_user to arangodb
                # if settings.SAVE_TO_ARANGODB:
                #     ArangoUserService.follow_band(band.userband.__dict__, activity.__dict__)

            return True
        except Exception as exception:
            raise exception

    @classmethod
    def get_email(cls, email):
        try:
            user_email = UserEmail.objects.get(email=email)
            if user_email:
                return user_email
        except Exception as e:
            cls.log_exception(e)
            return None
        return None

    @classmethod
    def gen_token(cls, user_id):
        text = str(user_id) + Utils.id_generator(10) + str(int(time.time()))
        hash_object = hashlib.md5(text.encode('utf-8'))
        return hash_object.hexdigest()

    @classmethod
    def get_by_email(cls, email):
        try:
            user = User.objects.get(email=email)
            return cls.get_user(user.pk)
        except User.DoesNotExist:
            return None

    @classmethod
    def get_users(cls, *args, **kwargs):
        limit = kwargs.get('limit', 20)
        offset = kwargs.get('offset', 0)
        search = kwargs.get('search', None)
        end = offset + limit
        filter = kwargs.get('filter', {})
        order_by = kwargs.get('order', '-id')
        includes = kwargs.get('includes', [])
        users = []
        if search:
            term = Q(username__icontains=search)
            user_ids = User.objects.values_list('id', flat=True) \
                           .order_by(order_by).filter(**filter).filter(term)[offset:end]
            count = User.objects.values_list('id', flat=True) \
                .order_by(order_by).filter(**filter).filter(term).count()
        else:
            user_ids = User.objects.values_list('id', flat=True).order_by(order_by).filter(**filter)[offset:end]
            count = User.objects.values_list('id', flat=True).order_by(order_by).filter(**filter).count()
        for id in user_ids:
            users.append(cls.get_user(id, includes=includes))
        return {
            'result': users,
            'count': count
        }

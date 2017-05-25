from django.db import transaction

from SocialNetwork_API.models import *
from SocialNetwork_API.services.base import BaseService
from datetime import datetime, timedelta


class ApiService(BaseService):

    @classmethod
    def save(cls, user, instance=None):
        try:
            token = cls.gen_token(user.id)
            api_obj = Api()
            api_obj.user_id = user.id
            api_obj.token = token
            expired = datetime.now() + timedelta(1, 0)
            api_obj.expired_at = expired
            api_obj.save()
            api_data = {'user': user, 'token': api_obj}
            return api_data

        except Exception as exception:
            cls.log_exception(exception)
            raise exception

    @classmethod
    def gen_token(cls, user_id):
        import time
        import hashlib
        text = str(user_id) + str(int(time.time()))
        hash_object = hashlib.md5(text.encode('utf-8'))
        return hash_object.hexdigest()

    @staticmethod
    def delete_session(token):
        Api.objects.get(token=token).delete()
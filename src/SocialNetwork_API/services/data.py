from django.db import transaction

from rest_framework.generics import get_object_or_404


from SocialNetwork_API.models import *
from SocialNetwork_API.services.base import BaseService


class DataService(BaseService):

    @classmethod
    def save(cls, request_data, instance=None):
        try:
            file = request_data.pop('file', None)
            data = instance if instance else Data()

            for key in request_data:
                setattr(data, key, request_data[key])

            file_info = None
            if file:
                return None
            with transaction.atomic():
                data.save()

                return data

        except Exception as exception:
            cls.log_exception(exception)
            raise exception


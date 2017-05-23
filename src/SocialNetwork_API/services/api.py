from django.db import transaction

from SocialNetwork_API.models import *
from SocialNetwork_API.services.base import BaseService

class ApiService(BaseService):

    @classmethod
    def save(cls, api_data, instance=None):
        try:
            data = instance if instance else Api()

            for key in api_data:
                setattr(data, key, api_data[key])

            with transaction.atomic():
                data.save()

                return data

        except Exception as exception:
            cls.log_exception(exception)
            raise exception
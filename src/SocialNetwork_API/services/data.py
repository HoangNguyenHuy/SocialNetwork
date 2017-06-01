from django.db import transaction

from os.path import join

from SocialNetwork_API.arango_services import ArangoDataService
from SocialNetwork_API.models import *
from SocialNetwork_API.services.base import BaseService
from sncore import settings


class DataService(BaseService):

    @classmethod
    def save(cls, request_data, instance=None):
        try:
            file = request_data.pop('file', None)
            data = instance if instance else Data()

            for key in request_data:
                setattr(data, key, request_data[key])

            with transaction.atomic():

                #save info data
                data.save()
                ArangoDataService.save_post(data.__dict__)
                # save file to local
                if file:
                    file_name = str(data.id)
                    local_file_path = join(settings.MEDIA_ROOT, file_name)
                    with open(local_file_path, 'wb') as dest:
                        for chunk in file.chunks():
                            dest.write(chunk)

                #update memory used
                from SocialNetwork_API.services import UserService
                user = UserService.get_user(data.user_id)
                user_data = {'memory_used': user.memory_used + data.capacity}
                UserService.save(instance=user, user_data=user_data)

            return data
        except Exception as exception:
            cls.log_exception(exception)
            raise exception


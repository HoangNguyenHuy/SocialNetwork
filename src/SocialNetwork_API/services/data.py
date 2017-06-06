import os
from os.path import join

from django.db import transaction

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
                    extension = data.name[data.name.rfind('.'):]
                    file_name = str(data.id)+extension
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

    @classmethod
    def get_data(cls, data_id):
        return ArangoDataService.get_data(data_id)

    @classmethod
    def get_data_of_user(cls, user_id):
        try:
            return (ArangoDataService.get_data_of_user(user_id))
        except Exception as e:
            raise e

    @classmethod
    def delete_data(cls, data):
        try:
            file_name = data.get('name')
            file_id = data.get('id')
            extension = file_name[file_name.rfind('.'):]
            name = str(file_id) + extension
            url = '{0}/{1}'.format(settings.MEDIA_ROOT, name)
            with transaction.atomic():

                # Delete comment from mysqldb
                data_id = data.get('id')
                file_data = Data.objects.filter(id=data_id)
                file_data.delete()

                # Delete comment from arangodb
                if settings.SAVE_TO_ARANGODB:
                    ArangoDataService.delete_data( data)

                os.remove(url)

                return True

        except Exception as exception:
            cls.log_exception(exception)
            raise exception
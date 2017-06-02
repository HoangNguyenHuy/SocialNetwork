import os
import shutil
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
    def download(cls, data_id):
        try:
            file_name = ArangoDataService.get_data(int(data_id),get_name=True)
            extension = file_name[file_name.rfind('.'):]
            old_file_name = str(data_id) + extension
            url_old = '{0}/{1}'.format(settings.MEDIA_ROOT, old_file_name)
            url_new = '{0}/{1}'.format(settings.DOWNLOAD_ROOT, file_name)
            # os.rename(url_old, url_new)
            shutil.copy2(url_old, url_new)
            return url_new

        except Exception as e:
            raise e

    @classmethod
    def get_data(cls, data_id):
        return ArangoDataService.get_data(data_id)
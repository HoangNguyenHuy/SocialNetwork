import shutil

from django.db import transaction

from SocialNetwork_API.arango_services import ArangoPostService, ArangoDownloadService, ArangoDataService
from SocialNetwork_API.models import *
from SocialNetwork_API.services.base import BaseService
from sncore import settings


class DownloadService(BaseService):

    @classmethod
    def get_download_history_of_user(cls, user_id):
        try:
            abc = ArangoDownloadService.get_download_history_of_user(str(user_id))
            return abc
        except Exception as exception:
            # cls.log_exception(exception)  # cái này là cái gì
            return None

    @classmethod
    def save(cls, data, instance=None):
        try:
            download = instance if instance else Download()

            for key in data:
                setattr(download, key, data[key])

            with transaction.atomic():
                download.save()
                ArangoDownloadService.save_download(download.__dict__)

            return download

        except Exception as exception:
            cls.log_exception(exception)
            raise exception

    @classmethod
    def get_post_of_friend(cls, user_id):
        try:
            return (ArangoPostService.get_post_of_friend(user_id))
        except Exception as e:
            raise e

    @classmethod
    def get_post_of_user(cls, user_id):
        try:
            return (ArangoPostService.get_post_of_user(user_id))
        except Exception as e:
            raise e

    @classmethod
    def download(cls, request):
        try:
            data_id = request.data['data_id']
            data = {'user_id': request.user.id, 'data_id': data_id}
            # copy file from media to download
            file_name = ArangoDataService.get_data(int(data_id), get_name=True)
            extension = file_name[file_name.rfind('.'):]
            old_file_name = str(data_id) + extension
            url_old = '{0}/{1}'.format(settings.MEDIA_ROOT, old_file_name)
            url_new = '{0}/{1}'.format(settings.DOWNLOAD_ROOT, file_name)
            # os.rename(url_old, url_new)
            shutil.copy2(url_old, url_new)

            # save info history
            DownloadService.save(data)

            return url_new

        except Exception as e:
            raise e

    @classmethod
    def delete_history(cls, data):
        try:

            with transaction.atomic():
                # Delete comment from mysqldb
                data_id = data.get('_key')
                file_data = Download.objects.filter(id=data_id)
                file_data.delete()

                # Delete comment from arangodb
                if settings.SAVE_TO_ARANGODB:
                    ArangoDownloadService.delete_download_history(data)

                return True

        except Exception as exception:
            cls.log_exception(exception)
            raise exception

    @classmethod
    def get_download_history(self, download_id):
        try:
            return ArangoDownloadService.get_download_history(download_id)
        except Exception as e:
            raise e

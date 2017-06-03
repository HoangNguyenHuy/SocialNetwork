from django.db import transaction

from SocialNetwork_API.arango_services import ArangoPostService, ArangoDownloadService
from SocialNetwork_API.models import *
from SocialNetwork_API.services.base import BaseService


class DownloadService(BaseService):

    # @classmethod
    # def get_download_history(cls, user_id):
    #     try:
    #         queryset = Posts.objects.all()
    #         post = get_object_or_404(queryset, pk=post_id)
    #         return post
    #     except Exception as exception:
    #         # cls.log_exception(exception)  # cái này là cái gì
    #         return None

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
import os
import logging
from django.db import connections


logger = logging.getLogger("project")
class BaseService:
    @staticmethod
    def last_query():
        print(connections['default'].queries)

    @classmethod
    def log_exception(cls, message):
        logger.exception(message)

    @classmethod
    def log_info(cls, message):
        logger.info(message)

    @classmethod
    def log_debug(cls, message):
        logger.debug(message)

    @classmethod
    def log(cls, message):
        logger.error(message)

    @classmethod
    def delete_file_from_local(cls, local_file_path, resize_file_path=None, thumb_file_path=None,
                               avatar_file_path=None):
        try:
            if local_file_path:
                os.remove(local_file_path)
        except:
            pass

        try:
            if resize_file_path:
                os.remove(resize_file_path)
        except:
            pass

        try:
            if thumb_file_path:
                os.remove(thumb_file_path)
        except:
            pass

        try:
            if avatar_file_path:
                os.remove(avatar_file_path)
        except:
            pass

    @classmethod
    def get_user_data(cls, user):
        if user:
            user_data = {
                'id': user.id,
                'country': user.userprofile.country,
                'state': user.userprofile.state,
                'city': user.userprofile.city,
                'longitude': user.userprofile.longitude,
                'latitude': user.userprofile.latitude,
            }
            return user_data
        else:
            return {}

    class Meta:
        abstract = True
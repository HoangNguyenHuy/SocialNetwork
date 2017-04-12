from django.db import transaction
from SocialNetwork_API.models.posts import Posts
from SocialNetwork_API.services.base import BaseService

class PostService(BaseService):

    @classmethod
    def save(cls, post_data):
        try:
            with transaction.atomic():
                task = Posts.objects.create(**post_data)
                return task
        except Exception as exception:
            cls.log_exception(exception)
            raise exception
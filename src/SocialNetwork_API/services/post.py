from django.db import transaction

from rest_framework.generics import get_object_or_404


from SocialNetwork_API.models.posts import Posts
from SocialNetwork_API.services.base import BaseService


class PostService(BaseService):

    @classmethod
    def get_post(cls, post_id):
        try:
            queryset = Posts.objects.all()#.filter(id=post_id)
            # return Posts.objects.get(pk=post_id)
            post = get_object_or_404(queryset, pk=post_id)
            return post
        except Exception as exception:
            # cls.log_exception(exception)  # cái này là cái gì
            return None


    @classmethod
    def save(cls, post_data):
        try:
            with transaction.atomic():
                task = Posts.objects.create(**post_data)
                return task
        except Exception as exception:
            cls.log_exception(exception)
            raise exception

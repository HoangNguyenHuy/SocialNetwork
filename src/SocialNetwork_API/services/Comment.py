from django.db import transaction

from rest_framework.generics import get_object_or_404


from SocialNetwork_API.models import *
from SocialNetwork_API.services.base import BaseService

class CommentService(BaseService):

    @classmethod
    def save(cls, comment_data, instance=None):
        try:
            comment = instance if instance else Comment()

            for key in comment_data:
                setattr(comment, key, comment_data[key])

            with transaction.atomic():
                comment.save()

                return comment

        except Exception as exception:
            cls.log_exception(exception)
            raise exception

    @classmethod
    def get_comment(cls, post_id):
        try:
            queryset = Comment.objects.all()
            comment = get_object_or_404(queryset, pk=post_id)

            return comment

        except Exception as exception:
            # cls.log_exception(exception)  # cái này là cái gì
            return None
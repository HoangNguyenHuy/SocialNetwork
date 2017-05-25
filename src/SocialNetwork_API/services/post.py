from django.db import transaction

from rest_framework.generics import get_object_or_404


from SocialNetwork_API.models import *
from SocialNetwork_API.services.base import BaseService


class PostService(BaseService):

    @classmethod
    def get_post(cls, post_id):
        try:
            queryset = Posts.objects.all()
            post = get_object_or_404(queryset, pk=post_id)
            return post
        except Exception as exception:
            # cls.log_exception(exception)  # cái này là cái gì
            return None


    @classmethod
    def save(cls, post_data, instance=None):
        try:
            post = instance if instance else Posts()

            for key in post_data:
                setattr(post, key, post_data[key])

            with transaction.atomic():
                post.save()

                return post

        except Exception as exception:
            cls.log_exception(exception)
            raise exception


    @classmethod
    def delete_comment(cls, post):
        try:
            with transaction.atomic():
                # Delete comment from mysqldb
                arr_comment_data = []
                comments = cls.get_all_comments_of_post(post.id)
                comments.append(post)
                for comment in comments:
                    comment_id = comment.id
                    comment.delete()

                    comment_data = comment.__dict__
                    comment_data['id'] = comment_id
                    arr_comment_data.append(comment_data)

                # Delete comment from arangodb
                # if settings.SAVE_TO_ARANGODB:
                #     ArangoCommentService.delete_comment(user.id, content.__dict__, arr_comment_data)

                return True
        except Exception as exception:
            cls.log_exception(exception)
            raise exception


    @classmethod
    def get_all_comments_of_post(cls, root_post_id):
        comments = Comment.objects.filter(post_id=root_post_id)
        parent_comments = list(comments)
        # cls.get_child_comments(parent_comments, comments)

        return parent_comments


    # @classmethod
    # def get_child_comments(cls, parent_comments, child_comments):
    #     for comment in child_comments:
    #         comments = Comment.objects.filter(post_id=comment.id)
    #         if len(comments) > 0:
    #             parent_comments.extend(comments)
    #             cls.get_child_comments(parent_comments, comments)
    #
    #     return parent_comments

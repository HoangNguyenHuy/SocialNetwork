from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework import status

from SocialNetwork_API.serializers import CommentSerializer
from SocialNetwork_API.views import BaseViewSet
from SocialNetwork_API.services import CommentService
from SocialNetwork_API.exceptions import ServiceException

class CommentViewSet(BaseViewSet):
    view_set = 'comment'
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        try:
            data = self.take_data_from_request(request)
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)

            # save data
            comment = serializer.save()

            comment_data = comment.__dict__
            if '_state' in comment_data:
                del comment_data['_state']

            return Response(comment_data, status=status.HTTP_200_OK)

        except Exception as exception:
            raise ServiceException(exception)

    def update(self, request, pk=None, *args, **kwargs):
        try:
            comment = self.get_and_check(pk)
            if comment.user_id != 1:
                raise exceptions.PermissionDenied()

            data = self.take_data_from_request(request, comment)

            serializer = self.serializer_class(instance=comment, data=data)
            serializer.is_valid(raise_exception=True)

            serializer.save(content=serializer.validated_data['comment']) # hoi a hao cai nay cai gi

            return Response(serializer.data)

        except Exception as exc:
            raise exc

    def delete(self, request, pk=None, *args, **kwargs):
        try:
            comment = self.get_and_check(pk)
            if comment.user_id != 1:
                raise exceptions.PermissionDenied()

            comment.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as exc:
            return exc

    @classmethod
    def get_and_check(self, pk):
        object = CommentService.get_comment(pk)

        if not object:
            raise exceptions.NotFound()

        return object

    @classmethod
    def take_data_from_request(cls, request, comment=None):

        data = request.data.copy()

        if not data:
            raise exceptions.APIException('update must be implemented.')

        data['user_id'] = request.user.id
        if comment:
            data['post_id'] = comment.post_id
            if 'reply_to_comment_id' in data:
                del data['reply_to_comment_id']
        return data
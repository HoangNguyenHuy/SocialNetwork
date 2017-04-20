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
            # take data from request
            # data = self.take_data_from_request(request)

            # validate data
            serializer = self.serializer_class(data=request.data)
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
            # serializer.save(content=request.data['content'],) # loi ko update du lieu

            serializer.save(content=serializer.validated_data['content'])

            return Response(serializer.data)

        except Exception as exc:
            raise exc


    @classmethod
    def get_and_check(self, pk):
        post = CommentService.get_comment(pk)
        if not post:
            raise exceptions.NotFound()

        return post

    @classmethod
    def take_data_from_request(cls, request, post=None):

        data = request.data.copy()
        if post:
            data['user_id'] = request.user.id
            if 'status' not in data:
                data['status'] = post.status

        return data
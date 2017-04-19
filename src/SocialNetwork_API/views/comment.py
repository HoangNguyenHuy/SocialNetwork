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


    # def create(self, request,  *args, **kwargs):
    #     try:
    #         data = self.take_data_from_request(request)
    #         serializer = PostSerializer(data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         post = serializer.save()
    #         post_data = post.__dict__
    #         if '_state' in post_data:
    #             del post_data['_state']
    #
    #         return Response(post_data, status=status.HTTP_200_OK)
    #
    #     except Exception as exception:
    #         raise exception

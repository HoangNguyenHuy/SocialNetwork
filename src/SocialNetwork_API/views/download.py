from rest_framework import exceptions,status
from rest_framework.response import Response

from SocialNetwork_API.exceptions import ServiceException
from SocialNetwork_API.serializers import DownloadSerializer
from SocialNetwork_API.services import PostService, DownloadService
from SocialNetwork_API.views import BaseViewSet

class DownloadViewSet(BaseViewSet):
    view_set = 'download'
    serializer_class = DownloadSerializer

    def list(self, request):
        try:
            return Response(PostService.get_post_of_user(request.user.id))
        except Exception as exception:
            raise exception

    def delete(self, request, pk=None, *args, **kwargs):
        try:
            post = self.get_and_check(pk)
            if post.user_id != request.user.id:
                raise exceptions.PermissionDenied()

            PostService.delete_comment(post)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as exception:
            raise ServiceException(exception)

    def create(self, request, *args, **kwargs):
        pass

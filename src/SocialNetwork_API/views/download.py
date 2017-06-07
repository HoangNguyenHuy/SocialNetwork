from rest_framework import exceptions,status
from rest_framework.response import Response

from SocialNetwork_API.const import StatusDataType
from SocialNetwork_API.exceptions import ServiceException
from SocialNetwork_API.serializers import DownloadSerializer
from SocialNetwork_API.services import PostService, DownloadService, DataService
from SocialNetwork_API.views import BaseViewSet
from django.utils import timezone
class DownloadViewSet(BaseViewSet):
    view_set = 'download'
    serializer_class = DownloadSerializer

    def list(self, request):
        try:
            return Response(DownloadService.get_download_history_of_user(request.user.id))
        except Exception as exception:
            raise exception

    def destroy(self, request, pk=None):
        data = self.get_and_check_history(str(pk))
        user_from = 'sn_users/'+str(request.user.id)
        if data.get('_from') != user_from:
            raise exceptions.PermissionDenied()
        DownloadService.delete_history(data=data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        self.get_and_check(request)
        url = DownloadService.download(request)
        url = url[url.rfind('/src'):]
        return Response(url)

    @classmethod
    def get_and_check(cls, request):
        if 'data_id' not in request.data:
            raise exceptions.APIException('data_id is required.')
        data_id = request.data['data_id']
        data = DataService.get_data(int(data_id))
        if not data:
            raise exceptions.APIException('data_id is invalid.')

        if data.get('data_status') == StatusDataType.PRIVATE and request.user.id != data.get('user_id'):
            raise exceptions.PermissionDenied()

        return data

    @classmethod
    def get_and_check_history(cls, pk):
        history = DownloadService.get_download_history(pk)
        if not history:
            raise exceptions.NotFound()
        return history
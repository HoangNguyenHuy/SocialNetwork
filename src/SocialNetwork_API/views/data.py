from rest_framework import status
from rest_framework.decorators import list_route
from rest_framework.response import Response

from rest_framework import exceptions
from SocialNetwork_API import permissions
from SocialNetwork_API.const import StatusDataType
from SocialNetwork_API.serializers import DataSerializer
from SocialNetwork_API.services import DataService
from SocialNetwork_API.views import BaseViewSet


class DataViewSet(BaseViewSet):

    serializer_class = DataSerializer

    def list(self, request):
        try:
            return Response(DataService.get_data_of_user(request.user.id))
        except Exception as exception:
            raise exception

    def delete(self, request, pk=None, *args, **kwargs):
        try:
            data = self.get_and_check(request)
            file_data = data.copy()
            if data.pop('user_id') != request.user.id:
                raise exceptions.PermissionDenied()
            DataService.delete_data(self,data=file_data)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as exc:
            return exc

    def create(self, request, *args, **kwargs):

        data = self.take_data_from_request(request)
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        post = serializer.save()
        post_data = post.__dict__
        if '_state' in post_data:
            del post_data['_state']

        return Response(post_data, status=status.HTTP_200_OK)

    @classmethod
    def get_and_check(cls, request):
        if 'data_id' not in request.data:
            raise exceptions.APIException('data_id is required.')
        data_id = request.data['data_id']
        data = DataService.get_data(int(data_id))
        if not data:
            raise exceptions.APIException('data_id is invalid.')
        if request.user.id != data.get('user_id'):
            raise exceptions.PermissionDenied()
        return data

    def take_data_from_request(cls, request):
        try:
            user = request.user
            upload_file = None
            status = StatusDataType.PRIVATE
            size = 0
            name = None

            if 'status' in request.data:
                status = request.data['status']

            if len(request.FILES) != 0:
                for key, file in request.FILES.items():
                    upload_file = file
                    del request.data[key]

                # upload_file.seek(0, 2) # move cursor from begin to end file
                size = upload_file.size
                name = upload_file.name
            data = {'user_id':user.id, 'file': upload_file, 'data_status': status, 'capacity': size, 'name': name}

        except Exception as e:
            raise e
        return data


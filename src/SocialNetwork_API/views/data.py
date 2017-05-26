
from rest_framework.response import Response

from SocialNetwork_API.const import StatusDataType
from SocialNetwork_API.serializers import DataSerializer
from SocialNetwork_API.views import BaseViewSet

class DataViewSet(BaseViewSet):

    serializer_class = DataSerializer

    def create(self, request, *args, **kwargs):

        data = self.take_data_from_request(request)
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        # follow_users = serializer.validated_data.pop('follow_users', None)
        # user = serializer.save(follow_users=follow_users)
        return Response(data)

    def take_data_from_request(cls, request):
        try:
            data = request.data.copy()
            user = request.user
            upload_file = None
            status = StatusDataType.PRIVATE
            size = 0
            name = None

            if 'status' in data:
                status = data['status']

            if len(request.FILES) != 0:
                for key, file in request.FILES.items():
                    upload_file = file
                    del request.data[key]

                upload_file.seek(0, 2) # move cursor from begin to end file
                size = upload_file.tell()
                name = upload_file.name
            data['user_id'] = user.id
            data['capacity'] = size
            data['name'] = name
            data['data_status'] = status
            data['file'] = upload_file
        except Exception as e:
            raise e
        return data

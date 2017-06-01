from rest_framework import status
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

        post = serializer.save()
        post_data = post.__dict__
        if '_state' in post_data:
            del post_data['_state']

        return Response(post_data, status=status.HTTP_200_OK)

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

                upload_file.seek(0, 2) # move cursor from begin to end file
                size = upload_file.tell()
                name = upload_file.name
            data = {'user_id':user.id, 'file': upload_file, 'data_status': status, 'capacity': size, 'name': name}

        except Exception as e:
            raise e
        return data

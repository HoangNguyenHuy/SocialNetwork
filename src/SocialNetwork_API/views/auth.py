from django.contrib.auth import user_logged_in, user_logged_out, user_login_failed, authenticate
from rest_framework import status, exceptions
from rest_framework.response import Response

from SocialNetwork_API.serializers import ApiSerializer, AuthTokenSerializer
from SocialNetwork_API.services import UserService
from SocialNetwork_API.views import BaseViewSet


class AuthViewSet(BaseViewSet):
    view_set = 'auth'
    serializer_class = AuthTokenSerializer

    def create(self, request):
        try:
            auth_serializer = self.serializer_class(data=request.data)
            auth_serializer.is_valid(raise_exception=True)

            user = self.check_login(request.data)
            serializer = ApiSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            api = serializer.save()
            api_data = api.__dict__
            if '_state' in api_data:
                del api_data['_state']

            return Response(api_data, status=status.HTTP_200_OK)
        except Exception as exception:
            raise exception

    def check_login(self, data):
        try:
            password = data.pop('password', None)

            if 'email' in data:
                email = data.pop('email', None)
                user = UserService.authenticate(email=email,username=None, password=password)
            if 'username' in data:
                username = data.pop('username', None)
                user = UserService.authenticate(username=username, email=None, password=password)
            from django.utils import timezone
            data['user'] = user
            # text = str(user_id) + str(int(time.time()))
            # data['token'] = hashlib.md5(text.encode('utf-8'))
            data['token'] = (user.id + timezone.now).decode(encoding='UTF-8',errors='strict')
            return data
        except Exception as aaa:
            return aaa


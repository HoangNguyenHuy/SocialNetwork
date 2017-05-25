from rest_framework.response import Response
from rest_framework import status, exceptions

from SocialNetwork_API.serializers import AuthTokenSerializer
from SocialNetwork_API.services import UserService, ApiService
from SocialNetwork_API.views import BaseViewSet


class AuthViewSet(BaseViewSet):
    view_set = 'auth'
    serializer_class = AuthTokenSerializer

    def create(self, request):
        try:
            auth_serializer = self.serializer_class(data=request.data)
            auth_serializer.is_valid(raise_exception=True)
            user = self.check_login(request.data)
            return Response(user, status=status.HTTP_200_OK)
        except Exception as exception:
            raise exception

    def delete(self, request):
        if request.user and request.user.is_authenticated():
            ApiService.delete_session(token=request.token)
            return Response(status=status.HTTP_200_OK)
        else:
            raise exceptions.NotAuthenticated()

    @classmethod
    def check_login(cls, data):
        try:
            password = data['password']
            if 'email' in data:
                email = data['email']
                user = UserService.authenticate(email=email,username=None, password=password)
            if 'username' in data:
                username = data['username']
                user = UserService.authenticate(username=username, email=None, password=password)
            user = ApiService.save(user)

            api_data = user['user'].__dict__
            if '_state' in api_data:
                del api_data['_state']
            api_data2 = user['token'].__dict__
            if '_state' in api_data2:
                del api_data2['_state']

            result = {'user': api_data, 'token': api_data2}
            return result
        except Exception as e:
            return None
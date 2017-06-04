from rest_framework import status

from SocialNetwork_API.serializers import UserSerializer, FriendSerialiser
from SocialNetwork_API.services import UserService
from SocialNetwork_API.views import BaseViewSet
from SocialNetwork_API.exceptions import ServiceException
from SocialNetwork_API import permissions

from sncore import settings

from rest_framework.response import Response
from rest_framework.decorators import list_route
from rest_framework.test import APIClient
from rest_framework import exceptions



class UserViewSet(BaseViewSet):

    view_set = 'user'
    serializer_class = UserSerializer

    def retrieve(self, request, pk=None, **kwargs):
        try:
            user = self.get_and_check(pk)
            serializer = UserSerializer(user)

            return Response(serializer.data)

        except Exception as exception:
            raise exception

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            user_data = user.__dict__
            if '_state' in user_data:
                del user_data['_state']

            return Response(serializer.data)
        except Exception as exception:
            raise ServiceException(exception)

    def update(self, request, pk=None, *args, **kwargs):
        try:
            user = UserService.get_user(pk)
            if user.id != request.user.id:
                raise exceptions.PermissionDenied()
            serializer = self.serializer_class(instance=user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer = UserSerializer(serializer.save())

            return Response(serializer.data)

        except Exception as exc:
            raise exc

    @list_route(methods=['post'], permission_classes=(permissions.IsAuthenticated,))
    def add_friend(self, request, *args, **kwargs):
        try:
            data = {'user_id': request.user.id, 'friend_id': request.data.get('friend_id')}
            serializer = FriendSerialiser(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.user_friend(request.user, serializer.validated_data['friend'])

            return Response(status=status.HTTP_200_OK)
        except Exception as exception:
            raise ServiceException(exception)

    @list_route(methods=['post'], permission_classes=(permissions.AllowAny,))
    def test_add_friend(self, request, *args, **kwargs):
        try:
            data = {'user_id': request.data.get('user_id'), 'friend_id': request.data.get('friend_id')}
            user = UserService.get_user(request.data.get('user_id'))
            serializer = FriendSerialiser(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.user_friend(user, serializer.validated_data['friend'])

            return Response(status=status.HTTP_200_OK)
        except Exception as exception:
            raise ServiceException(exception)
    @list_route(methods=['post'], permission_classes=(permissions.AllowAny,))
    def generate_user_data(self, request, *args, **kwargs):
        try:
            for i in range(1,1000,1):
                self.generate_single_user(i)

            return Response(status=status.HTTP_200_OK)

        except Exception as exception:
            raise exception

    @classmethod
    def generate_single_user(cls, i):
        client = APIClient()
        username = '{0}{1}'.format('user', str(i).zfill(4))
        email = '{0}{1}'.format(username, '@gmail.com')
        api_url = '{0}{1}'.format('http://', settings.API_URL)
        url = '{0}/{1}'.format(api_url, 'api/v1/user')
        client.credentials(HTTP_HOST='localhost', HTTP_DEVICE='postname', HTTP_APPID=1, HTTP_TYPE=8, HTTP_AGENT='agent')
        response = client.post(url, {
            'username': username,
            'email': email,
            'password': 'abc@123'
        }, format='json')

        return response

    @list_route(methods=['post'], permission_classes=(permissions.AllowAny,))
    def auto_add_friend(self, request):
        user_id = int(request.data.get('user_id'))
        n = int(request.data.get('numbers'))
        try:
            for friend_id in range(user_id+1, user_id + n, 1):
                self.ad_add_friend(user_id, friend_id)

            return Response(status=status.HTTP_200_OK)

        except Exception as exception:
            raise exception

    @classmethod
    def ad_add_friend(cls, user_id, friend_id):
        client = APIClient()
        api_url = '{0}{1}'.format('http://', settings.API_URL)
        url = '{0}/{1}'.format(api_url, 'api/v1/user/test_add_friend')
        client.credentials(HTTP_HOST='localhost', HTTP_DEVICE='postname', HTTP_APPID=1, HTTP_TYPE=8, HTTP_AGENT='agent')
        response = client.post(url, {
            'user_id': user_id,
            'friend_id': friend_id
        }, format='json')

        return response

    @classmethod
    def get_and_check(self, pk):
        post = UserService.get_user(pk)
        if not post:
            raise exceptions.NotFound()

        return post

    @list_route(methods=['post'], permission_classes=(permissions.AllowAny,))
    def test_add_post(self, request, *args, **kwargs):
        try:
            for i in range(11,1010,1):
                self.add_post(i)
            return Response(status=status.HTTP_200_OK)

        except Exception as exception:
            raise ServiceException(exception)

    def add_post(self, user_id):
        client = APIClient()
        api_url = '{0}{1}'.format('http://', settings.API_URL)
        url = '{0}/{1}'.format(api_url, 'api/v1/post/add_post')
        client.credentials(HTTP_HOST='localhost', HTTP_DEVICE='postname', HTTP_APPID=1, HTTP_TYPE=8, HTTP_AGENT='agent')
        response = client.post(url, {
            'user_id': user_id,
            'content': 'test arangodb query'
        }, format='json')

        return response
from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.decorators import list_route
from rest_framework.test import APIClient

from SocialNetwork_API import permissions
from SocialNetwork_API.exceptions import ServiceException
from SocialNetwork_API.serializers import FriendSerialiser
from SocialNetwork_API.services import UserService
from SocialNetwork_API.views import BaseViewSet
from sncore import settings


class AdminViewSet(BaseViewSet):
    view_set = 'admin'

    @list_route(methods=['post'], permission_classes=(permissions.AllowAny,))
    def generate_user_data(self, request, *args, **kwargs):
        try:
            start_number = 1
            numbers_user = 1000
            step = 1
            for i in range(start_number, numbers_user, step):
                self.generate_single_user(i)

            return Response(status=status.HTTP_200_OK)

        except Exception as exception:
            raise exception

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
    def generate_post(self, request, *args, **kwargs):
        try:
            start_user_id = 14
            end_user_id = 22
            step = 1
            for i in range(start_user_id, end_user_id, step):
                self.add_post_for_all_user(i)
            return Response(status=status.HTTP_200_OK)

        except Exception as exception:
            raise ServiceException(exception)

    def add_post_for_all_user(self, user_id):
        client = APIClient()
        api_url = '{0}{1}'.format('http://', settings.API_URL)
        url = '{0}/{1}'.format(api_url, 'api/v1/post/add_post')
        client.credentials(HTTP_HOST='localhost', HTTP_DEVICE='postname', HTTP_APPID=1, HTTP_TYPE=8, HTTP_AGENT='agent')
        response = client.post(url, {
            'user_id': user_id,
            'content': 'test arangodb query'
        }, format='json')

        return response

    @list_route(methods=['post'], permission_classes=(permissions.AllowAny,))
    def generate_friend(self,request, *args, **kwargs):
        try:
            start_user_id = 14
            end_user_id = 22
            step = 1
            numbers_friend = 3
            # start_friend_id = user_id[i] +1
            # end_friend_id = user_id[i] + number_friend
            # friend_step = 1
            for i in range(start_user_id, end_user_id+1, step):
                for j in range(i+1, i+numbers_friend+1, step):
                    if j > end_user_id:
                        break
                    self.ad_add_friend(i, j)
            return Response(status=status.HTTP_200_OK)

        except Exception as exception:
            raise ServiceException(exception)

    @classmethod
    def ad_add_friend(cls, user_id, friend_id):
        client = APIClient()
        api_url = '{0}{1}'.format('http://', settings.API_URL)
        url = '{0}/{1}'.format(api_url, 'api/v1/admin/test_add_friend')
        client.credentials(HTTP_HOST='localhost', HTTP_DEVICE='postname', HTTP_APPID=1, HTTP_TYPE=8, HTTP_AGENT='agent')
        response = client.post(url, {
            'user_id': user_id,
            'friend_id': friend_id
        }, format='json')

        return response

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

    # @list_route(methods=['post'], permission_classes=(permissions.AllowAny,))
    # def auto_add_friend(self, request):
    #     user_id = int(request.data.get('user_id'))
    #     n = int(request.data.get('numbers'))
    #     try:
    #         for friend_id in range(user_id + 1, user_id + n, 1):
    #             self.ad_add_friend(user_id, friend_id)
    #
    #         return Response(status=status.HTTP_200_OK)
    #
    #     except Exception as exception:
    #         raise exception
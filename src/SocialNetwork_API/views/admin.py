from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.decorators import list_route
from rest_framework.test import APIClient

from SocialNetwork_API import permissions
from sncore import settings


class AdminViewSet():
    view_set = 'admin'

    @list_route(methods=['post'], permission_classes=(permissions.AllowAny,))
    def generate_user_data(self, request, *args, **kwargs):
        try:
            # if not request.user.is_staff:
            #     raise exceptions.PermissionDenied()

            self.generate_single_user(10)

            return Response(status=status.HTTP_200_OK)

        except Exception as exception:
            raise exception

    @classmethod
    def generate_single_user(cls, i):
        client = APIClient()
        username = '{0}{1}'.format('user', str(i).zfill(4))
        email = '{0}{1}'.format(username, '@gmail.com')
        url = '{0}/{1}'.format(settings.API_URL, '/api/v1/user')
        # user_type = 2 if int(i) < 102 else 1
        # client.credentials(HTTP_HOST='localhost', HTTP_DEVICE='postname', HTTP_APPID=1, HTTP_TYPE=8, HTTP_AGENT='agent')
        response = client.post(url, {
            'username': username,
            'email': email,
            'password': 'abc@123'
        }, format='json')

        return response
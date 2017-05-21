from django.contrib.auth import user_logged_in, user_logged_out, user_login_failed
from rest_framework import status, exceptions
from rest_framework.response import Response

from SocialNetwork_API.views import BaseViewSet


class AuthViewSet(BaseViewSet):
    view_set = 'auth'

    def create(self, request):
        try:
            return Response({})
            # auth_serializer = self.serializer_class(data=request.data)
            # auth_serializer.is_valid(raise_exception=True)
            # client = request.client
            # # TODO: Make sure this client can try to login
            # remember_me = bool(request.data.get('remember_me', False))
            # id = auth_serializer.validated_data['user'].pk
            # return self.response_login(id=id, client=client, remember_me=remember_me)
        except Exception as exception:
            raise exception

def get_query_params(request, keys):
    rs = {}
    for key in keys:
        rs[key] = request.query_params.get(key, None)
    return rs

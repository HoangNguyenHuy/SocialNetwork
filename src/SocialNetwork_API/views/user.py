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

    @classmethod
    def get_and_check(self, pk):
        post = UserService.get_user(pk)
        if not post:
            raise exceptions.NotFound()

        return post

    @list_route(methods=['put'], permission_classes=(permissions.IsAuthenticated,))
    def change_password(self, request, *args, **kwargs):
        try:
            status_error = 0
            password = request.data.get('password', None)
            confirm_password = request.data.get('confirm_password', None)

            if not password and len(password.strip()) <= 6:
                status_error = 1
                raise exceptions.ValidationError('password must be at least 6 characters.')

            if password != confirm_password:
                status_error = 1
                raise exceptions.ValidationError('confirm_password is invalid.')

            UserService.set_new_password(request.user, password)

            return Response(status=status.HTTP_200_OK)
        except Exception as exception:
            if status_error == 1:
                raise exception
            else:
                raise ServiceException(exception)
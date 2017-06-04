from rest_framework import exceptions,status
from rest_framework import permissions
from rest_framework.decorators import list_route
from rest_framework.response import Response

from SocialNetwork_API.exceptions import ServiceException
from SocialNetwork_API.serializers import PostSerializer
from SocialNetwork_API.services import PostService
from SocialNetwork_API.views import BaseViewSet

class PostViewSet(BaseViewSet):
    view_set = 'post'
    serializer_class = PostSerializer

    def list(self, request):
        try:
            return Response(PostService.get_post_of_user(request.user.id))
        except Exception as exception:
            raise exception

    def retrieve(self, request, pk=None, **kwargs):
        try:
            post = self.get_and_check(pk)
            serializer = PostSerializer(post)

            return Response(serializer.data)

        except Exception as exception:
            raise exception

    def update(self, request, pk=None, *args, **kwargs):
        try:
            post = self.get_and_check(pk)
            if post.user_id != request.user.id:
                raise exceptions.PermissionDenied()

            data = self.take_data_from_request(request, post)

            serializer = self.serializer_class(instance=post, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(content=serializer.validated_data['content'])

            return Response(serializer.data)

        except Exception as exc:
            raise exc

    def delete(self, request, pk=None, *args, **kwargs):
        try:
            post = self.get_and_check(pk)
            if post.user_id != request.user.id:
                raise exceptions.PermissionDenied()

            PostService.delete_comment(post)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as exception:
            raise ServiceException(exception)

    def create(self, request, *args, **kwargs):
        try:
            data = self.take_data_from_request(request)
            serializer = PostSerializer(data=data)
            serializer.is_valid(raise_exception=True)

            post = serializer.save()
            post_data = post.__dict__
            if '_state' in post_data:
                del post_data['_state']

            return Response(post_data, status=status.HTTP_200_OK)

        except Exception as exception:
            raise exception

    @list_route(methods=['post', 'put'], permission_classes=(permissions.IsAuthenticated,))
    def get_list_post_of_user(self, request):
        try:
            user_id = request.data['user_id']
            return Response(PostService.get_post_of_user(user_id))
        except Exception as exception:
            raise exception

    @list_route(methods=['get'], permission_classes=(permissions.IsAuthenticated,))
    def get_post_of_friend(self, request):
        try:
            data = PostService.get_post_of_friend(request.user.id)
            # post_user = PostService.get_post_of_user(request.user.id)
            # data.append(post_user)
            return Response(data)
        except Exception as exception:
            raise exception

    @classmethod
    def get_and_check(self, pk):
        post = PostService.get_post(pk)
        if not post:
            raise exceptions.NotFound()

        return post

    @classmethod
    def take_data_from_request(cls, request, post=None):

        data = request.data.copy()
        if not data:
            raise exceptions.APIException('update must be implemented.')

        data['user_id'] = request.user.id
        if post:
            data['user_id'] = post.user_id
            if 'status' not in data:
                data['status'] = post.status

            if 'content' not in data:
                data['content'] = post.content

        return data

    @list_route(methods=['post'], permission_classes=(permissions.AllowAny,))
    def add_post(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            serializer = PostSerializer(data=data)
            serializer.is_valid(raise_exception=True)

            post = serializer.save()
            post_data = post.__dict__
            if '_state' in post_data:
                del post_data['_state']

            return Response(post_data, status=status.HTTP_200_OK)

        except Exception as exception:
            raise exception
from rest_framework import exceptions,status
from rest_framework.response import Response

from SocialNetwork_API.exceptions import ServiceException
from SocialNetwork_API.serializers import PostSerializer
from SocialNetwork_API.services import PostService
from SocialNetwork_API.views import BaseViewSet
from SocialNetwork_API.models import *

class PostViewSet(BaseViewSet):
    # view_set = 'post'
    serializer_class = PostSerializer

    def list(self, request):
        try:
            queryset = Posts.objects.all()
            serializer = PostSerializer(queryset, many=True)
            return Response(serializer.data)

        except Exception as exception:
            raise exception

    def retrieve(self, request, pk=None, **kwargs):
        try:
            post = self.get_and_check(pk)
            # queryset = Posts.objects.all().filter(user_id=pk)
            # post = get_object_or_404(post, pk=pk)
            serializer = PostSerializer(post)

            return Response(serializer.data)

        except Exception as exception:
            raise exception

    def update(self, request, pk=None, *args, **kwargs):
        try:
            post = self.get_and_check(pk)
            if post.user_id != 1:
                raise exceptions.PermissionDenied()

            data = self.take_data_from_request(request, post)

            serializer = self.serializer_class(instance=post, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(content=serializer.validated_data['content'])

            return Response(serializer.data)

        except Exception as exc:
            raise exc

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            post = self.get_and_check(pk)
            if post.user_id != 1:
                raise exceptions.PermissionDenied()
            post.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as exc:
            return exc

    def delete(self, request, pk=None, *args, **kwargs):
        try:
            post_id = int(pk)
            post = self.get_and_check(post_id)
            if post.user_id != request.user.id:
                raise exceptions.PermissionDenied()

            PostService.delete_comment(request.user, post)
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

        if post:
            data['user_id'] = post.user_id
            if 'status' not in data:
                data['status'] = post.status

            if 'content' not in data:
                data['content'] = post.content

        return data
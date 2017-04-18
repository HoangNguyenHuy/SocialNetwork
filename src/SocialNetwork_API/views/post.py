from rest_framework.generics import get_object_or_404
from rest_framework import exceptions,status
from rest_framework.response import Response

from SocialNetwork_API.serializers.post import PostSerializer
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

            # post = get_object_or_404(Posts.objects.all(), pk=pk)

            data = self.take_data_from_request(request, post)

            serializer = self.serializer_class(instance=post, data=data)
            serializer.is_valid(raise_exception=True)
            # serializer.save(content=request.data['content'],) # loi ko update du lieu

            serializer.save(content=serializer.validated_data['content'])

            return Response(serializer.data)

        except Exception as exc:
            raise exc


    def destroy(self, request, pk=None):
        try:
            post = Posts.objects.all().filter(pk=pk)
            post.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as exc:
            return exc


    def create(self, request):
        try:
            serializer = PostSerializer(data=request.data)
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
        if post:
            data['user_id'] = 1
            if 'status' not in data:
                data['status'] = post.status

        return data
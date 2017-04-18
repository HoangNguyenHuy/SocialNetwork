from rest_framework.generics import get_object_or_404

from SocialNetwork_API.serializers.post import PostSerializer
from SocialNetwork_API.views import BaseViewSet
from rest_framework.response import Response
from rest_framework import status
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

    def retrieve(self, request, pk=None):
        try:
            queryset = Posts.objects.all().filter(user_id=self.request.user.user_id)## sai
            post = get_object_or_404(queryset, pk=pk)
            serializer = self.serializer_class(post)
            return Response(serializer.data)

        except Exception as exception:
            raise exception

    def update(self, request, pk):
        try:
            post = get_object_or_404(Posts.objects.all(), pk=pk)
            serializer = self.serializer_class(post, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
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


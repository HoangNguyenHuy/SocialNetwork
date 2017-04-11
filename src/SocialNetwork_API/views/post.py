from SocialNetwork_API.serializers.post import PostSerializer
from SocialNetwork_API.views import BaseViewSet
from rest_framework.response import Response
from rest_framework import status

class PostViewSet(BaseViewSet):
    # view_set = 'post'
    serializer_class = PostSerializer

    def create(self, request):
        try:
            # data = request.data
            serializer = PostSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            post = serializer.save()
            post_data = post.__dict__
            if '_state' in post_data:
                del post_data['_state']
            return Response(post_data, status=status.HTTP_200_OK)

        except Exception as exception:
            raise exception


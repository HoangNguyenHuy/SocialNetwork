from SocialNetwork_API.models import Posts
from SocialNetwork_API.serializers import ServiceSerializer
from rest_framework import serializers
from SocialNetwork_API.services import PostService

class PostSerializer(ServiceSerializer):
    user_id = serializers.IntegerField(required=True)
    content = serializers.CharField(required=True)
    status = serializers.IntegerField(required=False)

    def create(self, validated_data):
        return PostService.save(validated_data)

    class Meta:
        model = Posts
        fields = ['id', 'user_id', 'content', 'status']

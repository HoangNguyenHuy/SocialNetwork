
from rest_framework import serializers
from rest_framework import exceptions

from SocialNetwork_API.const import StatusType
from SocialNetwork_API.models import Posts
from SocialNetwork_API.serializers import ServiceSerializer
from SocialNetwork_API.services import PostService

class PostSerializer(ServiceSerializer):
    user_id = serializers.IntegerField(required=True)
    content = serializers.CharField(required=True)
    status = serializers.IntegerField(required=False, default=StatusType.PUBLIC)

    def validate(self, data):
        # validate required fields
        self.validate_required_fields(data)

        return data

    @classmethod
    def validate_required_fields(cls, data):
        if data['status'] not in [StatusType.PUBLIC,StatusType.PRIVATE,StatusType.FRIEND,StatusType.CUSTOM]:
            raise exceptions.APIException('status is invalid.')

    def create(self, validated_data):
        return PostService.save(validated_data)

    def update(self, instance, validated_data):
        return PostService.save(validated_data, instance)


    class Meta:
        model = Posts
        fields = ['id', 'user_id', 'content', 'status']

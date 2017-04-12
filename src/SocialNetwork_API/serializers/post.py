from SocialNetwork_API.models import Posts
from SocialNetwork_API.serializers import ServiceSerializer
from rest_framework import serializers

class PostSerializer(ServiceSerializer):
    user_id = serializers.IntegerField(required=True)
    content = serializers.CharField(required=True)
    status = serializers.IntegerField(required=False)

    def create(self, validated_data):
        try:
            post = Posts.objects.create(**validated_data)
            post.save()
            return post

        except Exception as exception:
            raise exception

    # def create(self, validated_data):
    #     post = validated_data.pop('post')
    #     return PostService.save(user, validated_data)

    class Meta:
        model = Posts
        fields = ['id', 'user_id', 'content', 'status']

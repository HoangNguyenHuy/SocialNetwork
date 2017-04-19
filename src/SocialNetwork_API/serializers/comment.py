
from rest_framework import serializers
from rest_framework import exceptions


from SocialNetwork_API.models import Comment,Posts
from SocialNetwork_API.serializers import ServiceSerializer
from SocialNetwork_API.services import CommentService

class CommentSerializer(ServiceSerializer):
    user_id = serializers.IntegerField(required=True)
    post_id = serializers.IntegerField(required=False, allow_null=True)
    reply_to_comment_id = serializers.IntegerField(required=False, allow_null=True)
    comment = serializers.CharField(required=True)

    def validate(self, data):
        # validate required fields
        self.validate_required_fields(data)

        # validate reply_to_comment_id
        self.validate_comment_id(data)

        return data

    @classmethod
    def validate_comment_id(cls, data):
        try:
            if 'reply_to_comment_id' in data:
                comment = Comment.objects.get(pk=data['reply_to_comment_id'])
                if not comment or ('post_id' in data and comment.post_id != data['post_id']):
                    raise exceptions.APIException('reply_to_comment_id is invalid.')
        except:
            raise exceptions.APIException('reply_to_comment_id is invalid.')

    @classmethod
    def validate_required_fields(cls, data):
        if 'post_id' not in data:
            raise exceptions.APIException('post_id is required.')

        post = Posts.objects.get(pk=data['post_id'])
        if not post:
            raise exceptions.APIException('post_id does not exist.')

        if 'comment' not in data :
            raise exceptions.APIException('comment must include text or image.')


    def create(self, validated_data):
        return CommentService.save(validated_data)

    class Meta:
        model = Comment
        fields = ['id', 'user_id', 'post_id', 'comment', 'reply_to_comment_id']

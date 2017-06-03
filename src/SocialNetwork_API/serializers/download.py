
from rest_framework import serializers

from SocialNetwork_API.models import Download
from SocialNetwork_API.serializers import ServiceSerializer
from SocialNetwork_API.services import DownloadService

class DownloadSerializer(ServiceSerializer):
    data_id = serializers.IntegerField(required=True)
    user_id = serializers.IntegerField(required=True)

    def validate(self, data):
        return data

    def create(self, validated_data):
        return DownloadService.save(validated_data)

    class Meta:
        model = Download
        fields = ['id', 'user_id', 'data_id']

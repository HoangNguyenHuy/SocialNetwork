
from rest_framework import serializers
from rest_framework import exceptions

from SocialNetwork_API.const import StatusType
from SocialNetwork_API.models import Data
from SocialNetwork_API.serializers import ServiceSerializer
from SocialNetwork_API.services import DataService

class DataSerializer(ServiceSerializer):
    user_id = serializers.IntegerField(required=True)
    file = serializers.FileField(required=True)

    def validate(self, data):
        return data

    def create(self, validated_data):
        return DataService.save(validated_data)

    class Meta:
        model = Data
        fields = ['id', 'user_id', 'name', 'data_status', 'capacity']

from rest_framework import serializers
from rest_framework import exceptions

from SocialNetwork_API.const import *
from SocialNetwork_API.models import Data
from SocialNetwork_API.serializers import ServiceSerializer
from SocialNetwork_API.services import DataService, UserService

class DataSerializer(ServiceSerializer):
    file = serializers.FileField(required=True)
#coi lai cho nay nhung field null hay ko null
    def validate(self, data):
        if data['data_status'] not in [StatusDataType.PUBLIC, StatusDataType.PRIVATE, StatusDataType.FRIEND]:
            raise exceptions.APIException('status is invalid.')

        user = UserService.get_user(data['user_id'])
        if (user.memory_used + data['capacity'] > user.total_memory):
            raise exceptions.APIException('memory is not enough.')

        return data

    def create(self, validated_data):
        return DataService.save(validated_data)

    class Meta:
        model = Data
        fields = ['id', 'user_id', 'name', 'data_status', 'capacity']
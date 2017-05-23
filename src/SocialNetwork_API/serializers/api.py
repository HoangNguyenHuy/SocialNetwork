
from rest_framework import serializers

from SocialNetwork_API.models import Api
from SocialNetwork_API.serializers import ServiceSerializer
from SocialNetwork_API.services import *

class ApiSerializer(ServiceSerializer):

    def validate(self, data):
        return data

    def create(self, validated_data):
        return ApiService.save(validated_data)

    class Meta:
        model = Api
        fields = ['id', 'user', 'token']

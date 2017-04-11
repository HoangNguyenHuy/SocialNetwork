from rest_framework import serializers


class StringListField(serializers.ListField):
    child = serializers.CharField()


class ServiceSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        raise NotImplementedError('create must be implemented')

    def update(self, instance, validated_data):
        raise NotImplementedError('update must be implemented')

    def destroy(self):
        raise NotImplementedError('destroy must be implemented')


class ClientSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    device = serializers.CharField(required=True, max_length=64)
    app_id = serializers.CharField(required=True, max_length=64)
    type = serializers.IntegerField(required=True)
    ip = serializers.IPAddressField(required=False)
    token = serializers.CharField(required=False)
    version = serializers.CharField(max_length=10)
    user_agent = serializers.CharField(required=False)
    language = serializers.CharField(required=False, default='en')
    public_base = serializers.CharField(required=False, allow_null=True)
    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()


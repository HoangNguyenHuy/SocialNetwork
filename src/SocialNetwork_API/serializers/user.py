from rest_framework import exceptions
from rest_framework.validators import UniqueValidator

from SocialNetwork_API.serializers import ServiceSerializer, serializers
from SocialNetwork_API.const import UserType, ErrorMessage
from SocialNetwork_API.models import User, Friend
from SocialNetwork_API.services import UserService

class FriendSerialiser(serializers.Serializer):
    friend_id = serializers.IntegerField(required=True)
    user_id = serializers.IntegerField(required=True)

    def validate(self, data):
        if 'friend_id' in data:
            friend_id = data['friend_id']
        if 'user_id' in data:
            user_id = data['user_id']

        if user_id == friend_id:
            raise exceptions.ValidationError('friend_id must be different with user_id.')

        friend = UserService.get_user(friend_id)

        if not friend:
            error_message = ErrorMessage.DOES_NOT_EXIST.format('friend_id')
            raise exceptions.ValidationError(error_message)

        data['friend'] = friend
        return data

    @classmethod
    def user_friend(cls, user, friend):
        try:
            user_friend = UserService.get_user_friend(user.id, friend.id)
            if user_friend is not None:
                error_message = '{0} was friend by you.'.format(friend.username)
                raise exceptions.ValidationError(error_message)

            return UserService.user_friend(user, friend)
        except Exception as exception:
            raise exception

    class Meta:
        model = Friend
        fields = ['id', 'user_id', 'friend_user_id']
#     @classmethod
#     def unfollow_band(cls, user, band):
#         try:
#             user_follow = UserService.get_user_follow(user.id, band.id)
#             if user_follow is None:
#                 error_message = '{0} has not been followed by you.'.format(band.username)
#                 raise exceptions.ValidationError(error_message)
#
#             return UserService.unfollow_band(user, band, user_follow)
#         except Exception as exception:
#             raise exception
#
#




class UserSerializer(ServiceSerializer):
    username = serializers.CharField(required=True, max_length=30,
                                     validators=[UniqueValidator(queryset=User.objects.all(),
                                                                 message='username already in use.')])
    email = serializers.EmailField(required=True, max_length=254,
                                   validators=[UniqueValidator(queryset=User.objects.all(),
                                                               message='email already in use.')])
    password = serializers.CharField(required=True, min_length=6)







    # def to_representation(self, instance):
    #     ret = super(UserSerializer, self).to_representation(instance)
    #     if 'password' in ret:
    #         del ret['password']
    #     return ret
    #
    # def validate_user_type(self, value):
    #     # TODO: Not allow user set themself to admin or staff
    #     if not UserType.is_valid_type(value):
    #         raise exceptions.ValidationError(ErrorMessage.INVALID.format("user_type"))
    #     return value
    #
    # def validate(self, data):
    #     return data

    def create(self, validated_data):
        # for key in ['groups', 'user_permission']:
        #     if key in validated_data:
        #         del validated_data[key]
        user = UserService.save(validated_data)
        return user

    def update(self, instance, validated_data):
        return UserService.save(validated_data, instance)

    class Meta:
        model = User
        read_only_fields = ('id', )
        fields = (
            'id', 'email', 'username', 'password', 'first_name', 'last_name', 'sex', 'phone', 'dob',
            'date_joined', 'manager_id', 'is_superuser', 'is_staff', 'user_type','is_disabled',
        )
        extra_kwargs = {'password': {'write_only': True, 'hidden': True}}

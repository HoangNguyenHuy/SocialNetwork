from SocialNetwork_API.serializers import UserSerializer
from SocialNetwork_API.views import BaseViewSet
from SocialNetwork_API.exceptions import ServiceException

from rest_framework.response import Response

class UserViewSet(BaseViewSet):

    view_set = 'user'
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        try:
            # take data from request
            # data = self.take_data_from_request(request)
            #
            # if 'is_active' not in data:
            #     data['is_active'] = False
            abc = request.data.copy()
            serializer = self.serializer_class(data=abc)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            user_data = user.__dict__
            if '_state' in user_data:
                del user_data['_state']

            return Response(serializer.data)
        except Exception as exception:
            raise ServiceException(exception)

    @classmethod
    def take_data_from_request(cls, request, user=None):
        user_data = cls.take_user_data_from_request(request)
        profile_data = cls.take_profile_data_from_request(request)
        user_data['profile'] = profile_data
        band_data = {}

        if not user:
            if 'user_type' in request.data and int(request.data['user_type']) == UserType.FAN:
                user_type = UserType.FAN
            else:
                user_type = UserType.BAND

            user_data['user_type'] = user_type

            if user_type == UserType.BAND:
                band_data = cls.take_band_data_from_request(request)
                user_data['band'] = band_data

            # set default value
            cls.set_default_value(user_type, profile_data, user_data)
        else:
            if 'band_ids' in user_data:
                del user_data['band_ids']

            user_data['profile']['user_id'] = user.id
            user_type = user.user_type
            if user_type == UserType.BAND:
                band_data = cls.take_band_data_from_request(request)
                user_data['band'] = band_data
                user_data['band']['user_id'] = user.id
            else:
                fan_data = cls.take_fan_data_from_request(request)
                user_data['fan'] = fan_data
                user_data['fan']['user_id'] = user.id

        # update location
        if not user or ('address' in profile_data and profile_data['address'] != user.userprofile.address):
            location = cls.update_location(profile_data['address'])
            user_data['profile']['location_id'] = location['location_id']
            user_data['profile']['country'] = location['country']

        # update genre
        if user_type == UserType.BAND:
            if not user or ('genre' in band_data and band_data['genre'] != user.userband.genre):
                genres = cls.update_genre(band_data['genre'])
                user_data['band']['genre'] = genres['genre']
                user_data['band']['genre_ids'] = genres['genre_ids']

        return user_data

    def update(self, request, pk=None, *args, **kwargs):
        try:
        #     comment = self.get_and_check(pk)
        #     if comment.user_id != 1:
        #         raise exceptions.PermissionDenied()
        #
        #     data = self.take_data_from_request(request, comment)

            serializer = self.serializer_class(instance=request.data, data=request.data)
            serializer.is_valid(raise_exception=True)

            serializer.save(content=serializer.validated_data['comment']) # hoi a hao cai nay cai gi

            return Response(serializer.data)

        except Exception as exc:
            raise exc
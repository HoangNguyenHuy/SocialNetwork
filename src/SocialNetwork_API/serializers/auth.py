from django.contrib.auth import authenticate, user_logged_in
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework import exceptions

from SocialNetwork_API.services import UserService
from SocialNetwork_API.models import Api


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=True, style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.pop('username', None)
        email = attrs.pop('email', None)
        password = attrs.pop('password', None)

        if email and password:
            user = UserService.authenticate(email=email, password=password)
            if user:
                if not user.is_active:
                    msg = _('Your account is not activated.')
                    raise exceptions.ValidationError(msg)
                if user.is_disabled:
                    raise exceptions.ValidationError(_('Your account have been disabled.'))
            else:
                msg = _('Unable to log in with provided credentials.')
                raise exceptions.ValidationError(msg)
        elif username and password:
            user = authenticate(username=username, password=password, **attrs)
            if user:
                if not user.is_active:
                    msg = _('Your account is not activated.')
                    raise exceptions.ValidationError(msg)
                if user.is_disabled:
                    raise exceptions.ValidationError(_('Your account have been disabled.'))
            else:
                msg = _('Unable to log in with provided credentials.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Must include username/email and password.')
            raise exceptions.ValidationError(msg)
        user_logged_in.send(sender=user.__class__, user=user)
        attrs['user'] = user
        attrs['is_social_login'] = False
        attrs['provider'] = ''
        return attrs

    class Meta:
        model = Api
        fields = (
            'id', 'user_id', 'social_id', 'provider'
        )

from rest_framework import authentication, HTTP_HEADER_ENCODING
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from datetime import datetime
from django.utils import timezone
from SocialNetwork_API.exceptions import (
    BadHeaderParams, TokenExpired, AuthenticationFailed
)
from SocialNetwork_API.models.api import Api

def get_authorization_header(request):

    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    if isinstance(auth, type('')):
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth


class TokenAuthentication(authentication.BaseAuthentication):

    model = Api

    def authenticate(self, request):

        self._check_headers(request)
        auth = get_authorization_header(request).split()
        # khi login thi request nen duoc return ngay tai cho nay, vi minh ko care token
        if not auth or auth[0].lower() != b'token':
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise AuthenticationFailed(msg)

        return self.authenticate_credentials(token, request)

    def authenticate_credentials(self, key, request):
        try:
            token = self.model.objects.select_related('user').get(token=key)
        except self.model.DoesNotExist:
            raise AuthenticationFailed(_('Invalid request token.'))

        if not token.user.is_active:
            raise AuthenticationFailed(_('User inactive or deleted.'))

        if self.token_expired(token):
            #token.delete()
            raise TokenExpired()

        setattr(request, 'token', token.token)
        return (token.user, token)

    def _check_headers(self, request):
        if hasattr(request, 'bad_request_header'):
            raise BadHeaderParams()

    def token_expired(self, token):
        """
        Check token timeout
        :param token:
        :return: boolean
        """
        forever = timezone.make_aware(datetime.strptime(settings.REST_FRAMEWORK['EXPIRED_FOREVER'], '%Y-%m-%d %H:%M:%S'))
        if token.expired_at == forever:
            return False
        now = timezone.make_aware(datetime.now(), timezone.get_default_timezone())
        return token.expired_at < now

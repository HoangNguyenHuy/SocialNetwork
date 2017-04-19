from rest_framework import exceptions, status
from django.utils.translation import ugettext_lazy as _


class BadHeaderParams(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Invalid request headers')


class TokenExpired(exceptions.APIException):
    status_code = 432
    default_detail = _('Token expired')


class AuthenticationFailed(exceptions.APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('Incorrect authentication credentials.')


class Gone(exceptions.APIException):
    status_code = 410
    default_detail = _('Gone')


class ServiceException(exceptions.APIException):
    """
       Base class for REST framework exceptions.
       Subclasses should provide `.status_code` and `.default_detail` properties.
       """
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('A server error occurred.')

    def __init__(self, exception=None):
        if isinstance(exception, exceptions.ValidationError):
            error_fields = exception.detail
            error_message = ''
            for field in error_fields:
                error_message += error_fields[field][0] + '/ '

            self.status_code = status.HTTP_400_BAD_REQUEST
            self.detail = error_message
        elif isinstance(exception, exceptions.APIException):
            self.status_code = exception.status_code
            self.detail = exception.detail
        else:
            self.detail = exceptions.APIException.default_detail
            # for arg in exception.args:
            #     if isinstance(arg, str):
            #         self.detail = arg
            #         break


    def __str__(self):
        return self.detail



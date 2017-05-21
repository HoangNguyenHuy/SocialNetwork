class const(object):
    class ConstError(TypeError):
        pass  # base exception class

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't change const.%s" % name)
        if not name.isupper():
            raise self.ConstCaseError('const name %r is not all uppercase' % name)
        self.__dict__[name] = value

class StatusType(const):
    PUBLIC=1
    PRIVATE=2
    FRIEND=3
    CUSTOM=4

class UserType(const):
    USER = 1
    SUPERUSER = 2

    @classmethod
    def is_manager(cls, user_type):
        return user_type == cls.SUPERUSER

    @classmethod
    def is_valid_type(cls, user_type):
        return user_type in [
            cls.USER,
            cls.SUPERUSER
        ]

class SexType(const):
    MAN = 1
    WOMAN= 2
    UNKNOWN=3

class ResourceType(const):
    RS_USER = 1
    RS_LOCATION = 6


class ErrorMessage(const):
    REQUIRED = '{0} is required.'
    NULL = '{0} may not be null.'
    INVALID = '{0} is invalid.'
    BLANK = '{0} may not be blank.'
    MAX_LENGTH = '{0} must be less than or equal to {1} characters.'
    MIN_LENGTH = '{0} must be at least {1} characters.'
    MAX_VALUE = '{0} must be less than or equal to {1}.'
    MIN_VALUE = '{0} must be greater or equal to {1}.'
    ALREADY_EXISTS = '{0} already exists.'
    DOES_NOT_EXIST = '{0} does not exist.'
    PERMISSION_DENIED = 'Permission denied.'

# USER_TYPE_CHOICES = [
#     (UserType.USER, 'User'),
#     (UserType.SUPERUSER, 'Superuser'),
# ]
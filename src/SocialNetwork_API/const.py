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


# USER_TYPE_CHOICES = [
#     (UserType.USER, 'User'),
#     (UserType.SUPERUSER, 'Superuser'),
# ]
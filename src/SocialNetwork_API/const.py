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


class ActionType(const):
    FOLLOW = 1
    LIKE = 2
    COMMENT = 3
    REPLY = 4
    ADD = 5
    UNLIKE = 6
    UNCOMMENT = 7

class DataType(const):
    UPLOAD = 1
    DOWNLOAD = 2

class CollectionType(const):
    VERTEX = 1
    EDGE = 2

class ArangoVertex(const):
    ACTIVITY = 'sn_activities'
    COMMENT = 'sn_content_comment'
    DATA_NOTIFICATION = 'sn_data_notification'
    DATA = 'sn_datas'
    GROUP = 'sn_group'
    POST = 'sn_posts'
    USER_NOTIFICATION = 'user_notification'
    USER = 'sn_users'
    DOWNLOAD = 'sn_downloads'

class ArangoEdge(const):
    FRIEND = 'sn_friend'
    POST_DATA = 'sn_post_data'
    USER_DOWNLOAD = 'sn_user_download'
    USER_DATA = 'sn_user_data'
    USER_GROUP = 'sn_user_group'
    USER_POST = 'sn_user_post'
    POST_USER = 'sn_post_user'
    POST_COMMENT = 'sn_post_comment'
    DOWNLOAD_DATA = 'sn_download_data'


USER_FIELDS = [
    'id',
    'username',
    'email',
    'slug',
    'first_name',
    'last_name',
    'dob',
    'user_type',
    'is_active',
    'sex',
    'phone',
    'memory_used',
    'total_memory',
]

POST_COLLECTIONS = [
    ArangoVertex.POST,
    ArangoEdge.USER_POST
]

class StatusType(const):
    PUBLIC=1
    PRIVATE=2
    FRIEND=3
    CUSTOM=4

class StatusDataType(const):
    PUBLIC=1
    PRIVATE=2
    FRIEND=3

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
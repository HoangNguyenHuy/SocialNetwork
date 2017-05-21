from rest_framework import permissions, exceptions
from SocialNetwork_API.const import ErrorMessage


class InternalOnly(permissions.BasePermission):
    """
    Internal access only
    """

    def has_permission(self, request, view):
        password = request.META.get('HTTP_PASSWORD')
        if password:
            return True
        else:
            return False


class IsAuthenticated(permissions.BasePermission):
    """
    Global permission check for login user access
    """

    exception_methods = [
        'create_auth', 'create_user', 'retrieve_user', 'retrieve_content', 'retrieve_post', 'list_search',
        'band_activities_activity', 'fan_activities_activity'
    ]

    def has_permission(self, request, view):
        if self.get_exception_methods(view) in self.exception_methods:
            return True
        return request.user and request.user.is_authenticated()

    def get_exception_methods(self, view):
        action = view.action.lower() if view.action else ''
        view_set = getattr(view, 'view_set', '')
        method = action + "_" + view_set
        return method


class IsSuperuser(permissions.BasePermission):
    """
    Only staff can access this are
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated():
            return request.user.is_superuser


class NotAuthenticated(permissions.BasePermission):
    """
    Global check permission, only non login can access
    """

    def has_permission(self, request, view):
        return (not request.user or not request.user.is_authenticated())


def allow_access_user(current, user, raise_exception=True):
    """
    Check current user can access user data
    :param current: int user id or User object
    :param user: int manager id or User object
    :param raise_exception: set to True to raise exception
    :return: boolean allowed or not
    """
    allowed = False
    if not isinstance(current, int):
        user_id = current.manager_id
    else:
        user_id = current
    if not isinstance(user, int):
        manager_id = user.manager_id
    else:
        manager_id = user
    if manager_id == user_id:
        allowed = True
    if not allowed and raise_exception:
        raise exceptions.PermissionDenied()
    return allowed


def check_user_permission(request, user_id):
    if request.user.id != user_id:
        raise Exception(ErrorMessage.PERMISSION_DENIED)

AllowAny = permissions.AllowAny

from rest_framework import viewsets


class BaseViewSet(viewsets.ViewSet):
    activity_log = True


from SocialNetwork_API.views.post import PostViewSet
from SocialNetwork_API.views.auth import AuthViewSet
from SocialNetwork_API.views.comment import CommentViewSet
from SocialNetwork_API.views.user import UserViewSet
from SocialNetwork_API.views.admin import AdminViewSet
from SocialNetwork_API.views.data import DataViewSet
from SocialNetwork_API.views.download import DownloadViewSet

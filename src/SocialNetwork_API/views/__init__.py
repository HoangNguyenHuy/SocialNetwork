from rest_framework import viewsets


class BaseViewSet(viewsets.ViewSet):
    activity_log = True


from SocialNetwork_API.views.post import PostViewSet
from SocialNetwork_API.views.auth import AuthViewSet
from SocialNetwork_API.views.comment import CommentViewSet

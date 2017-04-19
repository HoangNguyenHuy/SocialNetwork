from django.conf.urls import url, include
from rest_framework import routers

from SocialNetwork_API.views import *

router = routers.SimpleRouter(trailing_slash=False)

router.register(r'post', PostViewSet, base_name="Post")
router.register(r'comment', CommentViewSet, base_name="Comment")

urlpatterns = [
    url(r'^', include(router.urls))
]

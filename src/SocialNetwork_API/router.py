from django.conf.urls import url, include
from rest_framework import routers

from SocialNetwork_API.views import *

router = routers.SimpleRouter(trailing_slash=False)

router.register(r'post', PostViewSet, base_name="Post")

urlpatterns = [
    url(r'^', include(router.urls))
]

from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include('SocialNetwork_API.router', namespace='v1', app_name='sn_core')),
]

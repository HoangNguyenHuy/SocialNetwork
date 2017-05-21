from django.db import models
from django.conf import settings

from SocialNetwork_API.models.timestamped import TimeStampedModel
from SocialNetwork_API.models.user_types import PositiveTinyIntegerField


class Api(TimeStampedModel):
    expired_at = models.DateTimeField(auto_now=False, default=settings.REST_FRAMEWORK['EXPIRED_FOREVER'])
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    device = models.CharField(max_length=64)
    ip = models.GenericIPAddressField()
    token = models.CharField(max_length=255)
    version = models.CharField(max_length=40)
    type = PositiveTinyIntegerField(default=0)
    app_id = models.CharField(max_length=64, default='')

    class Meta:
        db_table = 'sn_apis'

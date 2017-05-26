from django.db import models

from SocialNetwork_API.const import StatusDataType
from SocialNetwork_API.models.timestamped import TimeStampedModel


class Data(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    user_id = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=255, default='')
    data_status = models.PositiveIntegerField(default=StatusDataType.PRIVATE)
    capacity = models.BigIntegerField(default=0)
    approval = models.BooleanField(default=False)

    class Meta:
        db_table = 'sn_datas'
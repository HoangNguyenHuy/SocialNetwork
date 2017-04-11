from django.db import models
from SocialNetwork_API.models.timestamped import TimeStampedModel

class Download(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    data_id = models.PositiveIntegerField(default=0)
    user_id = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'sn_downloads'
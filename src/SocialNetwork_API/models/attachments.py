from django.db import models
from SocialNetwork_API.models.timestamped import TimeStampedModel

class Attachments(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    post_id = models.PositiveIntegerField(default=0)
    data_id = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'sn_attachments'
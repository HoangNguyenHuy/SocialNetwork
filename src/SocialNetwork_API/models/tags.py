from django.db import models
from SocialNetwork_API.models.timestamped import TimeStampedModel

class Tags (TimeStampedModel):
    id = models.AutoField(primary_key=True)
    user_id = models.PositiveIntegerField(default=0)
    post_id = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'sn_tags'
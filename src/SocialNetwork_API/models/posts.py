from django.db import models

from SocialNetwork_API.models.timestamped import TimeStampedModel
from SocialNetwork_API import const

class Posts(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    user_id = models.PositiveIntegerField(default=0)
    content = models.TextField()
    status = models.IntegerField(default=const.StatusType.PUBLIC)

    class Meta:
        db_table = 'sn_posts'
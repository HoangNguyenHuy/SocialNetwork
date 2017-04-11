from django.db import models
from SocialNetwork_API.models.timestamped import TimeStampedModel

class Friend(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    user_id = models.PositiveIntegerField(default=0)
    friend_user_id = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'sn_friends'
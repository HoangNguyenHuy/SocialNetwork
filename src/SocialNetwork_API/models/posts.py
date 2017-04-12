from django.db import models

from SocialNetwork_API.models.timestamped import TimeStampedModel


class Posts(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    user_id = models.PositiveIntegerField(default=0)
    content = models.TextField()
    status = models.IntegerField(default=1)

    class Meta:
        db_table='sn_posts'
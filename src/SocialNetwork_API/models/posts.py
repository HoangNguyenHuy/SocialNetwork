from django.db import models

from SocialNetwork_API.models.timestamped import TimeStampedModel


class Posts(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    user_id = models.PositiveIntegerField(default=0)
    content = models.TextField(max_length=1000, default='')
    status = models.CharField(max_length=255, default="Public")

    class Meta:
        db_table='sn_posts'
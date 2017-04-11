from django.db import models
from SocialNetwork_API.models.timestamped import TimeStampedModel

class Group(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    user_id = models.PositiveIntegerField(default=0)
    group_name = models.CharField(max_length=255, default='')
    number_of_members = models.IntegerField(default=1)

    class Meta:
        db_table = 'sn_groups'
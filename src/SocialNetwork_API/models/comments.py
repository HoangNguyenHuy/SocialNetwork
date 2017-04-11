from SocialNetwork_API.models.timestamped import TimeStampedModel
from django.db  import models

class Comment(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    post_id = models.PositiveIntegerField(default=0)
    user_id = models.PositiveIntegerField(default=0)
    reply_to_comment_id = models.PositiveIntegerField(default=0)
    comment = models.TextField(default='')

    class Meta:
        db_table = 'sn_comments'

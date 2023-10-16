from django.db import models
from users.models import User


from utils.models import TimeStamp


class FriendRequestStatus(models.IntegerChoices):
    SENT = 1
    ACCEPTED = 2
    REJECTED = 3


class FriendRequest(TimeStamp):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requests_sent")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requests_received")
    status = models.IntegerField(choices=FriendRequestStatus.choices)





class Friend(TimeStamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
    friend = models.ForeignKey(User, on_delete=models.CASCADE)

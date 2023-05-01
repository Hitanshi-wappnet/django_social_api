from django.db import models
from authentication.models import User


class Follow(models.Model):
    following = models.ForeignKey(User,
                                  related_name='following_user',
                                  on_delete=models.CASCADE,
                                  null=True, blank=True)
    follower = models.ForeignKey(User,
                                 related_name='follower_user',
                                 on_delete=models.CASCADE,
                                 null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower} following {self.following}'


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sender',
                               on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver',
                                 on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ('-timestamp',)

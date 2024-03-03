from django.db import models


class ReceivedMessage(models.Model):
    room = models.CharField(max_length=100)
    sender = models.CharField(max_length=100)
    is_group_chat = models.BooleanField(default=False)
    message = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.message


class SentMessage(models.Model):
    room = models.CharField(max_length=100)
    reply_to = models.ForeignKey(ReceivedMessage, on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    message = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.message

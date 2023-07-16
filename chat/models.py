from django.db import models
from django.contrib.auth.models import User


class ChatRoom(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(default='default_chatroom.jpg', upload_to='chatroom_pics')
    members = models.ManyToManyField(User, related_name='chat_rooms')
    is_direct_message = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        usernames = self.members.values_list('username', flat=True)
        return ', '.join(usernames)


class ChatMessage(models.Model):
    room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} in {self.room.name} at {self.timestamp}'

from django.db import models
from django.contrib.auth.models import User

class EmotionEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    emotion = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.date}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    psychologist_chat_id = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_messages')
    psychologist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='psychologist_messages')
    message_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ChatMessage {self.id} - {self.timestamp}"

# Вспомогательная функция для сохранения сообщения чата
def save_chat_message(user, psychologist, message_text):
    chat_message = ChatMessage(user=user, psychologist=psychologist, message_text=message_text)
    chat_message.save()
# psychological_companion/models.py
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Дополнительные поля для профиля пользователя
    # Например, поле для хранения чата с психологом

    def __str__(self):
        return self.user.username


class EmotionEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    emotion = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.date}"


from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date
from .models import UserProfile, EmotionEntry

class UserProfileModelTest(TestCase):
    def test_user_profile_creation(self):
        # Создаем пользователя
        user = User.objects.create_user(username="testuser", password="testpassword")

        # Создаем профиль пользователя
        user_profile = UserProfile.objects.create(user=user)

        # Проверяем, что профиль пользователя был успешно создан
        self.assertEqual(user_profile.user, user)

    def test_user_profile_string_representation(self):
        # Создаем пользователя
        user = User.objects.create_user(username="testuser", password="testpassword")

        # Создаем профиль пользователя
        user_profile = UserProfile.objects.create(user=user)

        # Проверяем строковое представление профиля пользователя
        self.assertEqual(str(user_profile), user.username)

class EmotionEntryModelTest(TestCase):
    def test_emotion_entry_creation(self):
        # Создаем пользователя
        user = User.objects.create_user(username="testuser", password="testpassword")

        # Создаем запись о настроении
        emotion_entry = EmotionEntry.objects.create(
            user=user,
            date=date.today(),
            emotion="Happy",
            description="Feeling great today!"
        )

        # Проверяем, что запись была успешно создана
        self.assertEqual(emotion_entry.user, user)

    def test_emotion_entry_string_representation(self):
        # Создаем пользователя
        user = User.objects.create_user(username="testuser", password="testpassword")

        # Создаем запись о настроении
        emotion_entry = EmotionEntry.objects.create(
            user=user,
            date=date.today(),
            emotion="Happy",
            description="Feeling great today!"
        )

        # Проверяем строковое представление записи о настроении
        expected_string = f"{user.username} - {date.today()}"
        self.assertEqual(str(emotion_entry), expected_string)

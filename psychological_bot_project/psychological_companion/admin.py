from django.contrib import admin
from .models import UserProfile, EmotionEntry

admin.site.register(UserProfile)
admin.site.register(EmotionEntry)
from typing import Iterable
from django.db import models
from django.contrib.auth.models import User
import uuid
from simple_history.models import HistoricalRecords
from googletrans import Translator
# from modeltranslation.translator import translator, TranslationOptions


class TODO(models.Model):
    status_choices = [
        ("c", "Completed"),
        ("p", "Pending"),
    ]
    #user_choices = [(user.id, user.username) for user in User.objects.all()]

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=20, choices=status_choices)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    history = HistoricalRecords(excluded_fields=['title_en', 'description_en', 'title_de', 'description_de'])

    def save(self, *args, **kwargs):
        translator = Translator()
        translated_title = translator.translate(self.title, dest='de').text
        translated_description = translator.translate(self.description, dest='de').text
        self.title_de = translated_title
        self.description_de = translated_description
        super().save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    otp = models.IntegerField(null=True, blank=True)
    language = models.CharField(max_length=20, default='de')

    def __str__(self):
        return self.user.username

class lang(models.Model):
    lang_choices = [
        ("en", "English"),
        ("de", "German"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=20, choices=lang_choices, default='de')

    def __str__(self):
        return self.language
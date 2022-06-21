from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

class Song(models.Model):
    title = models.CharField(max_length=150)
    artist = models.CharField(max_length=150)
    genre = models.CharField(max_length=150)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.artist + ' - ' + self.title

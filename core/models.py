from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.

User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    about = models.TextField(blank=True)
    profile_img = models.ImageField(upload_to='profile_images', default='default_image.png')

    def __str__(self):
        return self.user.username


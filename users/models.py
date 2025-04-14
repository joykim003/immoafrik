from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    whatsapp = models.CharField(max_length=20, blank=True, verbose_name="WhatsApp")
    messenger = models.URLField(max_length=200, blank=True, verbose_name="Messenger")
    address = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.username

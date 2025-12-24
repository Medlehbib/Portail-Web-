from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    ROLE_CHOICES = [
        ('Super_admin', 'Super_admin'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='admin')

    def __str__(self):
        return self.username
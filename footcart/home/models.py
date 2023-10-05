from django.contrib.auth.models import AbstractUser, Group
from django.db import models

class user_details(AbstractUser):
    phone_number = models.CharField(max_length=13)
    is_verified = models.BooleanField(default=False)

    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField(null=True,blank=True)
    gender = models.CharField(max_length=10,null=True,blank=True, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
        ])
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


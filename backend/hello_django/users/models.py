from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    eid = models.IntegerField(null=True, blank=True)
    ename = models.CharField(max_length=50, blank=True)
    esalary = models.FloatField(default=0.0)
    # password = models.CharField(max_length=20,null=True)

    username = models.CharField(max_length=150, unique=True, default='user')

    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=(('M', 'Male'), ('F', 'Female'), ('O', 'Other')), null=True, blank=True)
    hobbies = models.TextField(null=True, blank=True)
    isDeleted = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

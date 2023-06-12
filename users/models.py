from django.contrib.auth.models import AbstractUser
from django.db import models

from users.user_manager import UserManager


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    username = None
    email = models.EmailField(unique=True)
    organization = models.ForeignKey('users.Organization', blank=True, null=True, on_delete=models.PROTECT)
    objects = UserManager()


class Organization(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return self.name

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField()
    email = models.EmailField(unique=True)
    is_provider = models.BooleanField(default=False)

    class Meta:
        db_table = 'user'
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email

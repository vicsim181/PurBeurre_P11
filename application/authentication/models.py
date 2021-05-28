from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class User(AbstractUser):
    """
    Custom model class of User.
    """
    username = models.CharField(default='', max_length=20)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    registration_token = models.CharField(default='', max_length=200)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __str__(self) -> str:
        return self.first_name + ' ' + self.last_name + ' ' + self.email

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_email(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

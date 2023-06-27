from django.db import models
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
import jwt
from jwt import *


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):

        if username is None:
            raise TypeError('Users must have name')

        if email is None:
            raise TypeError('Users must have email address.')

        user = self.model(username=username, email=self.normalize_email(str(email)))
        user.set_password(str(password))
        user.save()

        return user

    def create_superuser(self, username, email, password):

        if password is None:
            raise TypeError('Superuser must have password')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_name()

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.username

    def _generate_jwt_name(self):
        dt = datetime.now() + timedelta(days=60)
        payload = {
            'id': self.pk,
            'exp': dt
        }
        token = jwt.encode(
            payload, 
            settings.SECRET_KEY, 
            algorithm='HS256'
        )

        return token

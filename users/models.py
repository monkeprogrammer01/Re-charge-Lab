import jwt
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from datetime import datetime, timedelta
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, name, surname, email, gender, password=None):
        if email is None:
            raise TypeError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), name=name, surname=surname, gender=gender)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, email, password, **extra_fields):
        if password is None:
            raise TypeError('Superusers must have a password.')

        name = extra_fields.get('name', 'Admin')
        surname = extra_fields.get('surname', 'User')
        gender = extra_fields.get('gender', 'other')

        user = self.create_user(
            email=email,
            password=password,
            name=name,
            surname=surname,
            gender=gender
        )
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.TextField(default="def")
    surname = models.TextField(default="def")
    gender = models.TextField(default="def")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt()

    def _generate_jwt(self):
        dt = datetime.now() + timedelta(days=1)
        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm="HS256")
        return token
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

class MyUserManager(BaseUserManager):
    use_in_migrations =True

    def _create_user(self, username, password, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuse must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField()
    avatar = models.ImageField('Аватар', upload_to='user_avatar/', null=True, blank=True)
    phone_number = models.CharField(verbose_name='Номер телефона', max_length=255)
    site = models.URLField('Ссылка на сайт',max_length=228, null=True, blank=True)
    bio = models.TextField('Био',null=True, blank=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.username}'


class Favorites(models.Model):
    post = models.ForeignKey('posts.Post', models.CASCADE, 'post_favorites')
    user = models.ForeignKey('users.User', models.SET_NULL,'user_favorites', null=True)
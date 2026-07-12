from django.contrib.auth.models import AbstractUser
from django.db import models

from core import constants


class User(AbstractUser):
    """Модель юзера."""

    email = models.EmailField(
        max_length=constants.EMAIL_LEN,
        verbose_name='Электронная почта',
        help_text='Электронная почта пользователя',
        null=True,
        blank=True
    )
    username = models.CharField(
        max_length=constants.USERNAME_LEN,
        unique=True,
        verbose_name='Ник',
        help_text='Виртуальное имя пользователя'
    )
    password = models.CharField(
        max_length=constants.PASSWORD_LEN,
        verbose_name='Пароль',
        help_text='Пароль пользователя'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

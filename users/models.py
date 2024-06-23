from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='email')
    phone = models.CharField(max_length=35, **NULLABLE, verbose_name='phone')
    token = models.CharField(max_length=100, **NULLABLE, verbose_name='token')  # 4
    slug = models.CharField(max_length=100, **NULLABLE, verbose_name='URL', unique=True)

    is_manager = models.BooleanField(default=False, blank=True, null=True, verbose_name='менеджер')  # права менеджера

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            ('can_view_all_users', 'can view all users'),
            ('can_block_users', 'can block users'),
        ]

    def __str__(self):
        return f'{self.email}'
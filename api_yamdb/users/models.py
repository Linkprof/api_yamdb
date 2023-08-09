from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

MAX_EMAIL_LENGTH = 254
MAX_ROLE_LENGTH = 9
MAX_NAME_LENGTH = 150
VALID_NAME = RegexValidator(r'^[\w.@+-]+\Z')


class User(AbstractUser):
    """Переопределенная модель User"""

    ROLES = {
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin')
    }

    username = models.CharField(
        'Имя пользователя',
        validators=[VALID_NAME],
        max_length=MAX_NAME_LENGTH,
        unique=True,
    )

    first_name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        blank=True
    )

    last_name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        blank=True
    )

    email = models.EmailField(
        'Электронная почта',
        unique=True,
        max_length=MAX_EMAIL_LENGTH,
    )

    role = models.CharField(
        max_length=MAX_ROLE_LENGTH,
        choices=ROLES,
        default=USER,
    )

    bio = models.TextField(
        'Биография',
        blank=True,
    )

    class Meta:
        ordering = ('username',)

    def __str__(self):
        return self.username

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Кастомный класс пользователя."""

    def __str__(self):
        return self.username


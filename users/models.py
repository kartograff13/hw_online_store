from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    """
    Кастомная модель пользователя с дополнительными полями.
    Email используется как уникальный идентификатор для входа.
    """

    username = None
    email = models.EmailField(unique=True, verbose_name="Электронная почта")

    avatar = models.ImageField(
        upload_to="users/avatars/", blank=True, null=True, help_text="Загрузите Ваш аватар", verbose_name="Аватар"
    )
    phone = PhoneNumberField(
        unique=True, blank=True, null=True, verbose_name="Телефон", help_text="Введите номер телефона"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email

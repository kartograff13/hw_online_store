from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    """Менеджер для модели User, использующий email в качестве идентификатора"""

    def create_user(self, email, password=None, **extra_fields):
        """Создаёт и сохраняет обычного пользователя"""
        if not email:
            raise ValueError("Email должен быть указан")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создаёт и сохраняет суперпользователя"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


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

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email

from django.db import models


class Category(models.Model):
    """Модель категории товара"""
    name = models.CharField(max_length=100, verbose_name="Наименование", unique=True)
    description = models.TextField(verbose_name="Описание", blank=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель товара"""
    name = models.CharField(max_length=100, verbose_name="Наименование", blank=True, unique=True)
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to="photos/", verbose_name="Изображение", blank=True, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Категория")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за покупку")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.name} ({self.price} руб.)"

from django.db import models


class Category(models.Model):
    """Модель категории товара"""

    name = models.CharField(max_length=100, verbose_name="Наименование", unique=True)
    description = models.TextField(verbose_name="Описание", blank=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель товара"""

    name = models.CharField(max_length=100, verbose_name="Наименование", unique=True)
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to="photos/", verbose_name="Изображение", blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Категория", related_name="products"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за покупку")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ("-created_at",)
        permissions = [
            ("can_unpublish_product", "Может отменять публикацию продукта"),
        ]

    def __str__(self):
        return f"{self.name} ({self.price} руб.)"


class Contact(models.Model):
    """Модель для хранения контактных данных"""

    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True, null=True)
    email = models.EmailField(verbose_name="Электронная почта", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
        ordering = ("-created_at",)

    def __str__(self):
        return f"Контакт: {self.first_name} {self.last_name} ({self.phone}, {self.email})."

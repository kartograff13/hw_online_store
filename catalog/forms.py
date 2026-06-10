import re

from django import forms
from django.core.exceptions import ValidationError

from .models import Product

FORBIDDEN_WORDS = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "price"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Введите название товара"}),
            "description": forms.Textarea(attrs={"placeholder": "Введите описание товара", "rows": 4}),
            "image": forms.FileInput(attrs={}),
            "category": forms.Select(attrs={}),
            "price": forms.NumberInput(attrs={"placeholder": "Введите цену", "min": "0", "step": "0.01"}),
        }
        labels = {
            "name": "Название товара",
            "description": "Описание",
            "image": "Изображение",
            "category": "Категория",
            "price": "Цена (руб.)",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == "category":
                field.widget.attrs["class"] = "form-control"
            else:
                field.widget.attrs["class"] = "form-control"

    def clean_name(self):
        """Валидация имени"""
        name = self.cleaned_data.get("name")
        if name:
            self._validate_forbidden_words(name)
            if len(name) < 3:
                raise forms.ValidationError("Название должно содержать минимум 3 символа")
        return name

    def clean_description(self):
        """Валидация описания"""
        description = self.cleaned_data.get("description")
        if description:
            self._validate_forbidden_words(description)
        return description

    def clean_price(self):
        """Валидация положительной цены"""
        price = self.cleaned_data.get("price")
        if price and price <= 0:
            raise ValidationError("Цена должна быть больше 0")
        return price

    def clean_image(self):
        """Валидация загружаемого изображения"""
        image = self.cleaned_data.get("image")
        if image:
            if image.size > 5 * 1024 * 1024:
                raise ValidationError("Размер изображения не должен превышать 5 МБ")

            allowed_content_types = ["image/jpeg", "image/png"]
            if image.content_type not in allowed_content_types:
                raise ValidationError("Допустимые форматы изображения: JPEG и PNG")
        return image

    @staticmethod
    def _validate_forbidden_words(text):
        """Проверяет наличие запрещенных слов в тексте (целые слова без учёта регистра)"""
        text_lower = text.lower()
        for word in FORBIDDEN_WORDS:
            if re.search(r"\b" + re.escape(word) + r"\b", text_lower):
                raise ValidationError(f"Поле содержит запрещенное слово: {word}.")

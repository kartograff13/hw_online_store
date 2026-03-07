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
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите название товара"}),
            "description": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Введите описание товара", "rows": 4}
            ),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "price": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Введите цену", "min": "0", "step": "0.01"}
            ),
        }
        labels = {
            "name": "Название товара",
            "description": "Описание",
            "image": "Изображение",
            "category": "Категория",
            "price": "Цена (руб.)",
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name:
            self._validate_forbidden_words(name)
            if len(name) < 3:
                raise forms.ValidationError("Название должно содержать минимум 3 символа")
            return name

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if description:
            self._validate_forbidden_words(description)
        return description

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price and price <= 0:
            raise ValidationError("Цена должна быть больше 0")
        return price

    def _validate_forbidden_words(self, text):
        """Проверяет наличие запрещенных слов в тексте (целые слова без учёта регистра)"""
        text_lower = text.lower()
        for word in FORBIDDEN_WORDS:
            if re.search(r"\b" + re.escape(word) + r"\b", text_lower):
                raise ValidationError(f"Поле содержит запрещенное слово: {word}.")

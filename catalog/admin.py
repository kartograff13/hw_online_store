from django.contrib import admin

from .models import Category, Contact, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "category")
    list_filter = ("category",)
    search_fields = ("name", "description")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "phone", "email", "created_at")
    search_fields = ("first_name", "last_name", "phone", "email")
    fieldsets = (
        ("Личная информация", {
            "fields": ("first_name", "last_name"),
        }),
        ("Контактные данные", {
            "fields": ("phone", "email"),
        }),
        ("Системные данные", {
            "fields": ("created_at", "update_at"),
        })
    )
    readonly_fields = ("created_at", "update_at")

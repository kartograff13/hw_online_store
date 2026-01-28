import re

from django.contrib import messages
from django.shortcuts import render, redirect


def home(request):
    """Контроллер главной страницы"""
    return render(request, "home.html")


def contacts(request):
    """Контроллер страницы контактов с обработкой формы обратной связи"""
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        message = request.POST.get("message", "").strip()

        if not all([name, phone, message]):
            messages.error(request, "Пожалуйста, заполните все поля формы.")
            return redirect("catalog:contacts")

        phone_pattern = r'^\+7\d{10}$'
        if not re.match(phone_pattern, phone):
            messages.error(request, "Неверный формат телефона. Введите номер в формате: +7XXXXXXXXXX")
            return redirect("catalog:contacts")


        messages.success(request, "Сообщение успешно отправлено. Мы свяжемся с Вами в ближайшее время!")
        return redirect("catalog:contacts")

    return render(request, "contacts.html")

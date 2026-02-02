from django.shortcuts import render
from django.contrib import messages
from .models import Category, Product, Contact


def home(request):
    """Контроллер главной страницы с выводом последних 5 продуктов в консоль"""
    latest_products = Product.objects.order_by('-created_at')[:5]

    print("ПОСЛЕДНИЕ 5 СОЗДАННЫХ ПРОДУКТОВ:")
    for i, product in enumerate(latest_products, 1):
        category_name = product.category.name if product.category else "Без категории"
        print(f"{i}. {product.name} - {product.price} руб. (Категория: {category_name})")

    context = {
        'latest_products': latest_products,
        'total_products': Product.objects.count(),
        'total_categories': Category.objects.count(),
    }
    return render(request, 'home.html', context)


def contacts(request):
    """Контроллер страницы контактов"""
    contact_info = Contact.objects.first()

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        message = request.POST.get('message', '').strip()

        if not name or not phone or not message:
            messages.error(request, 'Все поля обязательны для заполнения')
        else:
            clean_phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')

            if clean_phone.startswith('+'):
                if len(clean_phone) == 12 and clean_phone.startswith('+7') and clean_phone[2:].isdigit():
                    phone_valid = True
                else:
                    phone_valid = False
            elif clean_phone.startswith('8'):
                if len(clean_phone) == 11 and clean_phone[1:].isdigit():
                    phone_valid = True
                else:
                    phone_valid = False
            elif clean_phone.startswith('7'):
                if len(clean_phone) == 11 and clean_phone[1:].isdigit():
                    phone_valid = True
                else:
                    phone_valid = False
            else:
                phone_valid = False

            if not phone_valid:
                messages.error(request,
                               'Неверный формат телефона. Используйте: +7XXXXXXXXXX, 8XXXXXXXXXX или 7XXXXXXXXXX')
            else:
                if clean_phone.startswith('+'):
                    formatted_phone = clean_phone
                elif clean_phone.startswith('8'):
                    formatted_phone = '+7' + clean_phone[1:]
                else:
                    formatted_phone = '+' + clean_phone

                print("НОВОЕ СООБЩЕНИЕ ОБРАТНОЙ СВЯЗИ:")
                print(f"Имя: {name}")
                print(f"Телефон: {formatted_phone}")
                print(f"Сообщение: {message}")

                messages.success(request, 'Сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время.')

    context = {
        'contact': contact_info,
    }
    return render(request, 'contacts.html', context)

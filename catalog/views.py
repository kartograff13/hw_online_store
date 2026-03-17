from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import ProductForm
from .models import Category, Contact, Product


class HomeView(TemplateView):
    """Класс контроллера главной страницы с последними 5 добавленными товарами"""

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_products = Product.objects.order_by("-created_at")[:5]
        context["latest_products"] = latest_products
        context["total_products"] = Product.objects.count()
        context["total_categories"] = Category.objects.count()

        print("ПОСЛЕДНИЕ 5 СОЗДАННЫХ ПРОДУКТОВ:")
        for i, product in enumerate(latest_products, 1):
            category_name = product.category.name if product.category else "Без категории"
            print(f"{i}. {product.name} - {product.price} руб. (Категория: {category_name})")

        return context


class ContactView(View):
    """Страница контактов с формой обратной связи"""

    template_name = "contacts.html"

    def get(self, request):
        contact_info = Contact.objects.first()
        return render(request, self.template_name, {"contact": contact_info})

    def post(self, request):
        contact_info = Contact.objects.first()
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        message = request.POST.get("message", "").strip()

        if not name or not phone or not message:
            messages.error(request, "Все поля обязательны для заполнения")
        else:
            clean_phone = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
            phone_valid = False
            formatted_phone = None

            if clean_phone.startswith("+"):
                if len(clean_phone) == 12 and clean_phone.startswith("+7") and clean_phone[2:].isdigit():
                    phone_valid = True
                    formatted_phone = clean_phone
            elif clean_phone.startswith("8") or clean_phone.startswith("7"):
                if len(clean_phone) == 11 and clean_phone[1:].isdigit():
                    phone_valid = True
                    if clean_phone.startswith("8"):
                        formatted_phone = "+7" + clean_phone[1:]
                    else:
                        formatted_phone = "+" + clean_phone

            if not phone_valid:
                messages.error(
                    request, "Неверный формат телефона. Используйте: +7XXXXXXXXXX, 8XXXXXXXXXX или 7XXXXXXXXXX"
                )
            else:
                print("НОВОЕ СООБЩЕНИЕ ОБРАТНОЙ СВЯЗИ:")
                print(f"Имя: {name}")
                print(f"Телефон: {formatted_phone}")
                print(f"Сообщение: {message}")

                messages.success(request, "Сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время.")

        return render(request, self.template_name, {"contact": contact_info})


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Класс контроллера страницы с подробной информацией о товаре (только для авторизованных пользователей)"""

    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"


class CatalogListView(ListView):
    """Класс контроллера страницы каталога товаров с пагинацией"""

    model = Product
    template_name = "catalog.html"
    context_object_name = "all_products"
    paginate_by = 6
    ordering = ["-created_at"]


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Класс контроллера для добавления нового товара (только для авторизованных пользователей)"""

    model = Product
    form_class = ProductForm
    template_name = "add_product.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавить новый товар"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"'{self.object.name}' успешно добавлен.")
        return response

    def get_success_url(self):
        return reverse_lazy("catalog:product_detail", kwargs={"pk": self.object.pk})


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование товара (только для авторизованных пользователей)"""

    model = Product
    form_class = ProductForm
    template_name = "add_product.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Редактирование товара: {self.object.name}"
        return context

    def get_success_url(self):
        return reverse("catalog:product_detail", kwargs={"pk": self.object.pk})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление товара (только для авторизованных пользователей)"""

    model = Product
    template_name = "product_confirm_delete.html"
    success_url = reverse_lazy("catalog:catalog")
    context_object_name = "product"


class ProductUnpublishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Снимает продукт с публикации (только для модераторов"""

    permission_required = "catalog.can_unpublish_product"

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_published = False
        product.save()
        messages.success(request, f"Продукт '{product.name}' снят с публикации.")
        return redirect("catalog:product_detail", pk=pk)

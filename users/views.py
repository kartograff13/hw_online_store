from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import CreateView, UpdateView

from config import settings
from users.forms import ProfileForm, UserLoginForm, UserRegisterForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_link = self.request.build_absolute_uri(
            reverse("users:activate", kwargs={"uidb64": uid, "token": token})
        )

        subject = "Активация аккаунта в SkyStore"
        message = f"""
Здравствуйте, {user.username}!

Для активации Вашего аккаунта перейдите по ссылке:
{activation_link}

Если Вы не регистрировались на нашем сайте, проигнорируйте это письмо.

С уважением,
команда SkyStore
"""
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        messages.success(self.request, "Регистрация прошла успешно! Проверьте Вашу почту для активации аккаунта.")
        return redirect("users:login")


class ActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Аккаунт успешно активирован! Теперь Вы можете войти.")
            return redirect("users:login")
        else:
            messages.error(request, "Ссылка для активации недействительна или истекла")
            return redirect("users:login")


class CustomLoginView(LoginView):
    template_name = "users/login.html"
    authentication_form = UserLoginForm
    next_page = reverse_lazy("catalog:home")


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирования профиля текущего пользователя"""

    model = User
    form_class = ProfileForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Профиль успешно обновлен.")
        return response

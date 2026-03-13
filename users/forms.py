from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import User


class UserRegisterForm(UserCreationForm):
    """Форма регистрации нового пользователя (только email и пароль)"""

    email = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Введите Email"})
    )
    password1 = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Введите пароль"})
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Подтвердите пароль"}),
    )

    class Meta:
        model = User
        fields = ("email",)

    def save(self, commit=True):
        """Сохраняет пользователя, устанавливая email в качестве username"""
        user = super().save(commit=False)
        user.email = self.cleaned_data.get("email")
        user.username = self.cleaned_data.get("email")

        if commit:
            user.save()

        return user


class UserLoginForm(AuthenticationForm):
    """Форма входа пользователя (email вместо username)"""

    username = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Введите Email"})
    )
    password = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Введите пароль"})
    )

    def clean(self):
        """Аутентификация пользователя по emile и паролю"""
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data


class ProfileForm(forms.ModelForm):
    """Форма редактирования профиля пользователя (имя, фамилия, аватар, телефон)"""

    class Meta:
        model = User
        fields = ("first_name", "last_name", "avatar", "phone")
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Имя"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Фамилия"}),
            "avatar": forms.FileInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Номер телефона"}),
        }
        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
            "avatar": "Аватар",
            "phone": "Телефон",
        }

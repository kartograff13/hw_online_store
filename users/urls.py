from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import ActivateView, CustomLoginView, ProfileUpdateView, RegisterView

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="users:login"), name="logout"),
    path("activate/<uidb64>/<token>/", ActivateView.as_view(), name="activate"),
    path("profile/", ProfileUpdateView.as_view(), name="profile"),
]

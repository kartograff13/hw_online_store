from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import catalog, contacts, home, product_detail

app_name = CatalogConfig.name

urlpatterns = [
    path("", home, name="home"),
    path("contacts/", contacts, name="contacts"),
    path("products/<int:pk>/", product_detail, name="product_detail"),
    path("catalog/", catalog, name="catalog"),
]

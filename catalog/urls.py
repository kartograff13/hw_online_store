from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import (
    CatalogListView,
    ContactView,
    HomeView,
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductUpdateView,
)

app_name = CatalogConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contacts/", ContactView.as_view(), name="contacts"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("catalog/", CatalogListView.as_view(), name="catalog"),
    path("add_product/", ProductCreateView.as_view(), name="add_product"),
    path("products/update/<int:pk>", ProductUpdateView.as_view(), name="product_update"),
    path("products/delete/<int:pk>", ProductDeleteView.as_view(), name="product_delete"),
]

from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import HomeView, ContactView, ProductDetailView, CatalogListView, ProductCreateVeiw

app_name = CatalogConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contacts/", ContactView.as_view(), name="contacts"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("catalog/", CatalogListView.as_view(), name="catalog"),
    path("add_product/", ProductCreateVeiw.as_view(), name="add_product"),
]

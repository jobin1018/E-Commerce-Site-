from django.contrib import admin
from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    path("", views.store, name="store"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("update_item/", views.UpdateItem, name="update_item"),
    path("process_order/", views.ProcessOrder, name="process_order"),
    path("category/<int:pk>/", views.ProductByCategory, name="product_by_category"),
    path("product/<int:pk>/", views.ProductDetail, name="product_detail"),
]

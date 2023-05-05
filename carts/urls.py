from django.urls import path

from . import views

urlpatterns = [
    path("accounts/cart/", views.CartDetailView.as_view()),
    path("products/<int:product_id>/cart/", views.CartProductView.as_view())
]

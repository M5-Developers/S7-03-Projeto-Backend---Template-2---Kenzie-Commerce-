from django.urls import path

from . import views

urlpatterns = [
    path("accounts/cart/", views.CartDetailView.as_view()),
    path("products/<int:product_id>/cart/", views.CartProductView.as_view()),
    path("products/<int:product_id>/cart/<int:cart_id>/", views.CartProductDetailView.as_view()),
    path("products/<int:product_id>/cart/<int:cart_id>/delete/", views.CartProductDeleteView.as_view())
]

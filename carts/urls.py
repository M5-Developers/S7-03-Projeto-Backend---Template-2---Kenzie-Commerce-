from django.urls import path

from . import views

urlpatterns = [
    path("accounts/cart/", views.CartView.as_view()),
]

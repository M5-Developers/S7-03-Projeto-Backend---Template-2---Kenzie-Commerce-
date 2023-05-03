from django.urls import path

from . import views

urlpatterns = [
    path("accounts/<int:account_id>/cart/", views.CartView.as_view()),
]

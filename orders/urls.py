from django.urls import path
from .views import OrderView, OrderViewDetail, OrderInAccountView

urlpatterns = [
    path("orders/", OrderView.as_view()),
    path("orders/<int:pk>/", OrderViewDetail.as_view()),
    path("accounts/orders/", OrderInAccountView.as_view()),
]

from django.urls import path

from .views import OrderView,OrderViewDetail

urlpatterns = [
    path("orders/", OrderView.as_view()),
    path("orders/<int:pk>/", OrderViewDetail.as_view()),
]

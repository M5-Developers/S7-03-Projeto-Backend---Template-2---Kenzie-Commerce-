from django.urls import path
from .views import AccountView, AccountDetailView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("accounts/", AccountView.as_view()),
    path("accounts/<int:account_id>/", AccountDetailView.as_view()),
    path("login/", TokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
]

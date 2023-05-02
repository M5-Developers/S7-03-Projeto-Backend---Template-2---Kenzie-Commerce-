from django.urls import path
from . import views
from address.views import AddressView, AddressByIdView

urlpatterns = [
    path("address/", views.AddressView.as_view()),
    path("address/<int:address_id>/", views.AddressByIdView.as_view())
]
from django.urls import path
from address.views import AddressView, AddressByIdView

urlpatterns = [
    path("address/", AddressView.as_view()),
    path("address/<int:address_id>/", AddressByIdView.as_view())
]
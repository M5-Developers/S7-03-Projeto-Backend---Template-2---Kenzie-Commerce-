from django.urls import path

from . import views

urlpatterns = [
    path("products/", views.AlbumView.as_view()),
]

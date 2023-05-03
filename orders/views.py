from django.shortcuts import render
from rest_framework import generics
from .serializers import OrderSerializer,Order
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class OrderView(generics.ListCreateAPIView):

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

    serializer_class=OrderSerializer
    queryset=Order.objects.all()

    def perform_create(self, serializer):
        user=self.request.pop('user')
        serializer.save(user=user)

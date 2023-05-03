from django.shortcuts import render
from rest_framework import generics
from .serializers import OrderSerializer,Order
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsSeller

class OrderView(generics.ListCreateAPIView):

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

    serializer_class=OrderSerializer
    queryset=Order.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderViewDetail(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsSeller]

    serializer_class=OrderSerializer
    queryset=Order.objects.all()

    

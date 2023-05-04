from django.shortcuts import render
from rest_framework import generics
from .serializers import OrderSerializer,Order
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsSeller
from utils.sendEmail import send_html
from accounts.models import Account

class OrderView(generics.ListCreateAPIView):

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

    serializer_class=OrderSerializer
    queryset=Order.objects.all()

    def perform_create(self, serializer):
        send_html(self.request.user.email,'Pending')
        serializer.save(user=self.request.user)

class OrderViewDetail(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsSeller]

    serializer_class=OrderSerializer
    queryset=Order.objects.all()

    def perform_update(self, serializer):
        order_pk=self.kwargs['pk']
        order_obj= Order.objects.get(id=order_pk)
        user_email=Account.objects.get(id=order_obj.user_id).email
        send_html(user_email,self.request.data['status'])
        
        serializer.save()
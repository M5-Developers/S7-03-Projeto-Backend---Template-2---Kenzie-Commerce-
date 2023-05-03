from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from accounts.permissions import IsSeller
from . import models, serializers

class ProductView(generics.ListCreateAPIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [IsAuthenticatedOrReadOnly, IsSeller]
	
	queryset = models.Product.objects.all()
	serializer_class = serializers.ProductSerializer

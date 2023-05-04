from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from . import models, serializers

class ProductView(generics.ListCreateAPIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [IsAuthenticatedOrReadOnly]
	
	queryset = models.Product.objects.all()
	serializer_class = serializers.ProductSerializer

	def perform_create(self, serializer):
		serializer.save(seller_id=self.request.user.id)
	
	def get_queryset(self):
		queryset = super().get_queryset()

		name = self.request.GET.get('name')
		category = self.request.GET.get('category')
		
		if name:
			queryset = queryset.filter(name__icontains=name)
			return queryset

		if category:
			queryset = queryset.filter(category__icontains=category)
		
		return queryset

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [IsAuthenticatedOrReadOnly]
	
	queryset = models.Product.objects.all()
	serializer_class = serializers.ProductSerializer

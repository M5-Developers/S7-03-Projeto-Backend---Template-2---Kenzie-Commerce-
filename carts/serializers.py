from rest_framework import serializers
from . import models

class CartProductSerializer(serializers.ModelSerializer):
	def update(self, instance, validated_data):
		instance.quantity += validated_data['quantity']
		instance.save()
		return instance
	
	class Meta:
		model = models.CartProduct
		fields = '__all__'
		read_only_fields = ['cart', 'product']

class CartSerializer(serializers.ModelSerializer):
	cart_products = CartProductSerializer(many=True)
	
	class Meta:
		model = models.Cart
		fields = '__all__'

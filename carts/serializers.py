from rest_framework import serializers
from . import models


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartProduct
        fields = '__all__'
        read_only_fields = ['product', 'cart']

class CartSerializer(serializers.ModelSerializer):
	cart_products = CartProductSerializer(many=True)
	
	class Meta:
		model = models.Cart
		fields = '__all__'

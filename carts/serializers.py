from rest_framework import serializers
from . import models

class CartProductSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        # if self.context['request'].method == 'PATCH':
        #     return super().update(instance, validated_data)
        
        instance.quantity += validated_data['quantity']
        instance.save()
        return instance
    
    class Meta:
        model = models.CartProduct
        fields = '__all__'
        read_only_fields = ['cart', 'product']

class CartSerializer(serializers.ModelSerializer):
    cart_products = serializers.SerializerMethodField()

    class Meta:
        model = models.Cart
        fields = ['account_id', 'cart_products']
        depth = 1

    def get_cart_products(self, obj):
        cart_products = obj.cart_products.all()
        return CartProductSerializer(cart_products, many=True).data
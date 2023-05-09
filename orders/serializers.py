from rest_framework import serializers
from .models import Order, ProductOrder

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=[
            'id',
            'user_id',
            'status',
            'created_at',
            'products'
        ]
        depth=1
        extra_kwargs={
            'id':{'read_only':True},
            'created_at':{'read_only':True},
            'user_id':{'read_only':True}
        }

class ProductOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOrder
        fields = [
            'order_id',
            'product'
            'quantity',
		]
        extra_kwargs={
            'quantity':{'read_only': True},
        }

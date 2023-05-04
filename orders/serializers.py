from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model=Order
        fields=[
            'id',
            'user_id',
            'status',
            'created_at'
        ]
        depth=1
        extra_kwargs={
            'id':{'read_only':True},
            'created_at':{'read_only':True},
            'user_id':{'read_only':True}
        }

from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
	def create(self, validated_data):
		return Product.objects.create(**validated_data)
	
	class Meta:
		model = Product
		fields = '__all__'
		extra_kwargs = {
			"seller": {
				"read_only": True
			}
		}

from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):

	available=serializers.SerializerMethodField()
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

	def get_available(self,obj):
		if obj.quantity>0:
			return True
		return False
	
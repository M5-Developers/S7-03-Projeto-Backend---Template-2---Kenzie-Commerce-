from django.db import models
from django.core.validators import MinValueValidator

class Status(models.TextChoices):
    PENDING = "Pending"
    INPROGRESS="In progress"
    DELIVERED= "Delivered"

class Order(models.Model):
	user=models.ForeignKey('accounts.Account',on_delete=models.CASCADE,related_name='orders')
	status=models.CharField(max_length=20,choices=Status.choices,default=Status.PENDING)
	created_at=models.DateTimeField(auto_now_add=True)
	products = models.ManyToManyField(
		'products.Product',
        through='orders.ProductOrder',
        related_name='orders'
	)
    
class ProductOrder(models.Model):
	quantity = models.IntegerField(validators=[MinValueValidator(0)])
	order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='orders'
	)
	product = models.ForeignKey(
		'products.Product',
        on_delete=models.CASCADE,
        related_name='order_products'
	)

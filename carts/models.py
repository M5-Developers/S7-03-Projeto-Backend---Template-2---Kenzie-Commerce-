from django.db import models
from django.core.validators import MinValueValidator

class Cart(models.Model):
    account = models.OneToOneField(
        'accounts.Account',
		on_delete=models.CASCADE
    )

class CartProduct(models.Model):
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    cart = models.ForeignKey(
        'carts.Cart',
        on_delete=models.CASCADE,
        related_name='cart_products'
	)
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='products'
	)

from django.db import models

class Cart(models.Model):
    account = models.OneToOneField(
        'accounts.Account',
		on_delete=models.CASCADE
    )

class CartProduct(models.Model):
    quantity = models.IntegerField()
    cart = models.ForeignKey(
        'carts.Cart',
        on_delete=models.CASCADE,
        related_name='carts'
	)
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='products'
	)

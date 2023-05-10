from django.db import models
from django.core.validators import MinValueValidator

class CategoryChoices(models.TextChoices):
	SHIRT = 'Shirt'
	T_SHIRT = 'T-Shirt'
	JACKETS = 'Jackets'
	PANTS = 'Pants'
	SHORTS = 'Shorts'
	UNDERWEAR = 'Underwear'


class Product(models.Model):
	name = models.CharField(max_length=127)
	category = models.CharField(
		max_length=20,
		choices=CategoryChoices.choices
	)
	price = models.DecimalField(max_digits=8, decimal_places=2)
	quantity = models.IntegerField(validators=[MinValueValidator(0)])
	available = models.BooleanField(default=True)
	seller = models.ForeignKey(
		'accounts.Account',
		on_delete=models.CASCADE,
		related_name='products'
	)

	
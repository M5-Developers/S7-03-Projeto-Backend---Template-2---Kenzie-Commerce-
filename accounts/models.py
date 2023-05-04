from django.db import models
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):
	email = models.EmailField(max_length=127, unique=True)
	first_name = models.CharField(max_length=127)
	last_name = models.CharField(max_length=127)
	type = models.CharField(max_length=127, default='')

	address = models.OneToOneField(
		"address.Address",
		on_delete=models.SET_NULL,
		related_name="account",
		null=True
	)
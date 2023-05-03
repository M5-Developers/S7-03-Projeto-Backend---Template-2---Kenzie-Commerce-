from django.db import models

class Cart(models.Model):
    account = models.OneToOneField(
        'accounts.Account',
		on_delete=models.CASCADE
    )

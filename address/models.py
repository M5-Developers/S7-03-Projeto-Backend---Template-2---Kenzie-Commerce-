from django.db import models
from accounts.models import Account

# Create your models here.
class Address(models.Model):
    street = models.CharField(max_length=127)
    cep = models.CharField(max_length=8)
    number = models.CharField(max_length=127)

    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ["id"]
from django.db import models
from users.models import User

# Create your models here.
class Address(models.Model):
    street = models.CharField(max_length=127)
    cep = models.IntegerField(max_length=8)
    number = models.CharField(max_length=127)

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="user_address"
    )

    class Meta:
        ordering = ["id"]
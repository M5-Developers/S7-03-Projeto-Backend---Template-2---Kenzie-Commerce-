from django.db import models

# Create your models here.
class Address(models.Model):
    street = models.CharField(max_length=127)
    cep = models.CharField(max_length=8)
    number = models.CharField(max_length=127)
    
    class Meta:
        ordering = ["id"]
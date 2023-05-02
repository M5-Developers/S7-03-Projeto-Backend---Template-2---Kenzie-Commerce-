from django.db import models

class Status(models.TextChoices):
    ANDAMENTO="EM ANDAMENTO"
    ENTREGUE= "ENTREGUE"
    DEFAULT="Pedido REALIZADO"

class Order(models.Model):
    user=models.ForeignKey('accounts.Account',on_delete=models.CASCADE)
    status=models.CharField(max_length=20,choices=Status.choices,default=Status.DEFAULT)
    created_at=models.DateTimeField(auto_now_add=True)
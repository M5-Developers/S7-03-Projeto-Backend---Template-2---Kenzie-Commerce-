from django.db import models

class Status(models.TextChoices):
    PENDING = "Pending"
    INPROGRESS="In progress"
    DELIVERED= "Delivered"

class Order(models.Model):
    user=models.ForeignKey('accounts.Account',on_delete=models.CASCADE)
    status=models.CharField(max_length=20,choices=Status.choices,default=Status.PENDING)
    created_at=models.DateTimeField(auto_now_add=True)
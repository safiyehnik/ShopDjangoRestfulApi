from django.db import models


# Create your models here.
class Order(models.Model):
    order_number = models.CharField(max_length=100)
    total_price = models.PositiveIntegerField()
    total_off = models.PositiveIntegerField()
    user_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

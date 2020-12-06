from django.db import models


# Create your models here.
class Product(models.Model):
    category = models.ForeignKey(to='products.category', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    description = models.CharField(max_length=200)
    off = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.name

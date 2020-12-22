from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to="img/products", null=True, blank=True)

    def __str__(self):
        return self.name

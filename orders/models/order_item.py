from django.db import models
from django.utils.translation import gettext_lazy as _


class OrderItem(models.Model):
    product = models.ForeignKey(to='products.Product', on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name=_('Product'))
    order = models.ForeignKey(to='orders.Order', on_delete=models.CASCADE, verbose_name=_('Order'))
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    price = models.PositiveIntegerField(verbose_name=_('Price'))
    off = models.PositiveIntegerField(verbose_name=_('Off'))
    quantity = models.PositiveIntegerField(null=True, blank=True, verbose_name='Quantity')

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")

    def __str__(self):
        return self.product.name
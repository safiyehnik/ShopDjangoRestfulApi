from django.contrib import admin

# Register your models here.
from orders.models.order import Order
from orders.models.order_item import OrderItem


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'price', 'off')
    

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'total_price', 'total_off', 'user_name', 'first_name', 'last_name')


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
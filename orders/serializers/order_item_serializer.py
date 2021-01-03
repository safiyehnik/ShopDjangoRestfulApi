from rest_framework import serializers
from orders.models.order_item import OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["order", "product", "name", "price", "off", "quantity"]

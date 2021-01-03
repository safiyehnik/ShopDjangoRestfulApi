from rest_framework import serializers
from orders.models.order import Order
from orders.serializers.order_item_serializer import OrderItemSerializer


class OrderSerializer(serializers.ModelSerializer):
    order_item = OrderItemSerializer(many=True, source='orderitem_set')

    class Meta:
        model = Order
        fields = ['order_number', 'order_status', 'total_cost', 'total_off', 'phone_number', 'first_name', 'last_name',
                  'order_item']

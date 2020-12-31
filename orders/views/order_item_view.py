from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from orders.models.order import Order
from orders.models.order_item import OrderItem
from orders.serializers.order_item_serializer import OrderItemSerializer
from orders.serializers.order_serializer import OrderSerializer
from products.models.product import Product


class OrderItemView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, product_id):
        try:
            return Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise Http404

    def create_order_item_object(self, product_obj):
        obj = OrderItem.objects.create(product=product_obj,
                                       # order=order_obj,
                                       name=product_obj.name,
                                       price=product_obj.price,
                                       off=product_obj.off)
        return obj

    def create_order_object(self, user, order_items, total_cost, total_off):
        order_obj = Order.objects.create(phone_number=user.phone_number,
                                         first_name=user.first_name,
                                         last_name=user.last_name,
                                         total_off=total_off,
                                         total_cost=total_cost)
        for order_item in order_items:
            order_item.order = order_obj
        return order_obj

    def post(self, request):
        serializer = OrderItemSerializer(data=request.data, many=True)
        user = request.user
        if serializer.is_valid():
            basket = request.data
            total_cost = 0
            total_off = 0
            order_items = []
            for item in basket:
                product_id = item['product_id']
                product_obj = self.get_object(product_id)
                order_item_obj = self.create_order_item_object(product_obj)
                order_items.append(order_item_obj)
                total_cost += product_obj.price
                total_off += product_obj.off * product_obj.price
            object_order = self.create_order_object(user, order_items, total_off, total_cost)
            serializer2 = OrderSerializer(instance=object_order)
            return Response(serializer2.data, status=201)
        return Response(serializer.errors, status=400)

    def get(self,request):
        object_order = self.create_order_object()
        serializer = OrderSerializer(instance=object_order)
        return Response(data=serializer.data)
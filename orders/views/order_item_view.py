from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from orders.models.order import Order
from orders.models.order_item import OrderItem
from orders.serializers.order_serializer import OrderSerializer
from products.models.product import Product


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000


class OrderItemView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    pagination_class = StandardResultsSetPagination
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['phone_number']
    search_fields = ['phone_number']

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(data={"error": "User is not login"}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data

        if not data:
            return Response(data={"error": "Request body is empty"}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(data, list):
            return Response(data={"error": "Request body should be a list"}, status=status.HTTP_400_BAD_REQUEST)

        product_obj_list = []
        product_quantity_list = []
        for product in data:
            product_id = product.get("product_id")
            product_quantity = product.get("quantity")

            try:
                product_obj = Product.objects.get(id=product_id)
                product_obj_list.append(product_obj)
                product_quantity_list.append(product_quantity)
            except Product.DoesNotExist:
                return Response(data={"error": f"Product with {product_id} not found "},
                                status=status.HTTP_404_NOT_FOUND)

        total_cost_with_off = 0
        total_cost_without_off = 0

        for product_obj, product_quantity in zip(product_obj_list, product_quantity_list):
            product_price = product_obj.price
            product_off = product_obj.off
            calculate_price_off = product_price - ((product_off / 100) * product_price)  # for one product
            total_cost_with_off += calculate_price_off * product_quantity
            total_cost_without_off += product_price * product_quantity

        total_off = total_cost_without_off - total_cost_with_off

        order_obj = Order.objects.create(
            phone_number=request.user.phone_number,
            first_name=request.user.first_name,
            last_name=request.user.last_name,
            total_cost=total_cost_with_off,
            total_off=total_off
        )

        for product_obj, product_quantity in zip(product_obj_list, product_quantity_list):
            OrderItem.objects.create(
                product=product_obj,
                order=order_obj,
                name=product_obj.name,
                price=product_obj.price,
                off=product_obj.off,
                quantity=product_quantity
            )
        serializer = OrderSerializer(instance=order_obj)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return Response(data={"error": "User is not login"}, status=status.HTTP_401_UNAUTHORIZED)

        queryset = self.filter_queryset(Order.objects.filter(phone_number=request.user.phone_number))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        # serializer = OrderSerializer(instance=Order.objects.all(), many=True)
        # return Response(data=serializer.data, status=status.HTTP_200_OK)


    # def get_object(self, product_id):
    #     try:
    #         return Product.objects.get(id=product_id)
    #     except Product.DoesNotExist:
    #         raise Http404
    #
    # def create_order_item_object(self, product_obj):
    #     obj = OrderItem.objects.create(product=product_obj,
    #                                    # order=order_obj,
    #                                    name=product_obj.name,
    #                                    price=product_obj.price,
    #                                    off=product_obj.off)
    #     return obj
    #
    # def create_order_object(self, user, order_items, total_cost, total_off):
    #     order_obj = Order.objects.create(phone_number=user.phone_number,
    #                                      first_name=user.first_name,
    #                                      last_name=user.last_name,
    #                                      total_off=total_off,
    #                                      total_cost=total_cost)
    #     for order_item in order_items:
    #         order_item.order = order_obj
    #     return order_obj
    #
    # def post(self, request):
    #     serializer = OrderItemSerializer(data=request.data, many=True)
    #     user = request.user
    #     if serializer.is_valid():
    #         basket = request.data
    #         total_cost = 0
    #         total_off = 0
    #         order_items = []
    #         for item in basket:
    #             product_id = item['product_id']
    #             product_obj = self.get_object(product_id)
    #             order_item_obj = self.create_order_item_object(product_obj)
    #             order_items.append(order_item_obj)
    #             total_cost += product_obj.price
    #             total_off += product_obj.off * product_obj.price
    #         object_order = self.create_order_object(user, order_items, total_off, total_cost)
    #         serializer2 = OrderSerializer(instance=object_order)
    #         return Response(serializer2.data, status=201)
    #     return Response(serializer.errors, status=400)
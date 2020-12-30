from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.views import APIView

from orders.models.order import Order
from orders.models.order_item import OrderItem
from orders.serializers.order_item_serializer import OrderItemSerializer
from orders.serializers.order_serializer import OrderSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class OrderView(mixins.ListModelMixin,
                mixins.DestroyModelMixin,
                mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                mixins.CreateModelMixin,
                viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ['order_number']
    # search_fields = ['order_number']

    @action(detail=True, methods=["GET"])
    def items(self, request, pk, *args, **kwargs):

        queryset = self.filter_queryset(OrderItem.objects.filter(order_id=pk))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = OrderItemSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = OrderItemSerializer(queryset, many=True)
        return Response(serializer.data)

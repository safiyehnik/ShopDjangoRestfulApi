from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.serializers.order_item_serializer import OrderItemSerializer


class OrderItemView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = OrderItemSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=404)
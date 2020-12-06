from django.http import Http404
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from products.serializers.product_serializer import ProductSerializer
from products.models.product import Product
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError


class ProductView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        product_obj = Product.objects.all()
        serializer = ProductSerializer(instance=product_obj, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

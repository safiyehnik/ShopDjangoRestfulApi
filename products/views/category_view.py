from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from products.serializers.category_serializer import CategorySerializer
from products.models.category import Category


class CategoryView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        category_obj = Category.objects.all()
        serializer = CategorySerializer(instance=category_obj, many=True, context={"request": request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 201)
        return Response(serializer.errors, 400)

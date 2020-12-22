from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, filters
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from products.models.category import Category
from products.models.product import Product
from products.serializers.category_serializer import CategorySerializer
from products.serializers.product_serializer import ProductSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class CategoryView(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    pagination_class = StandardResultsSetPagination
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    permission_classes = (AllowAny,)

    @action(detail=True, methods=["GET"])
    def products(self, request, pk, *args, **kwargs):
        queryset = self.filter_queryset(Product.objects.filter(category_id=pk))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ProductSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# class CategoryDetailView(APIView):
#     permission_classes = (AllowAny,)
#
#     def get_object(self, pk):
#         try:
#             return Category.objects.get(id=pk)
#         except Category.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk):
#         category_obj = self.get_object(pk)
#         serializer = CategoryUpdateSerializer(instance=category_obj, context={"request": request})
#         return Response(data=serializer.data)
#
#     def put(self, request, pk):
#         category_obj = self.get_object(pk)
#         serializer = CategoryUpdateSerializer(instance=category_obj, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data)
#         return Response(serializer.errors, 400)
#
#     def delete(self, request, pk):
#         category_obj = self.get_object(pk)
#         category_obj.delete()
#         return Response()





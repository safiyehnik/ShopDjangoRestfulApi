from django.urls import re_path
from rest_framework.routers import DefaultRouter

from products.views.category_view import CategoryView
from products.views.product_view import ProductView

router = DefaultRouter()
router.register(r'products', ProductView, basename='product-url')
router.register(r'categories', CategoryView, basename='category_url')

urlpatterns = [
    # re_path(r'categories/?$', CategoryView.as_view()),
    # re_path(r'categories/(?P<pk>\d+)/?$', CategoryDetailView.as_view()),
    # re_path(r'categories/(?P<pk>\d+)/products/?$', CategoryView.as_view()),

]
urlpatterns += router.urls

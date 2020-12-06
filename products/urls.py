from django.urls import re_path

from products.views.category_view import CategoryView
from products.views.category_detail_view import CategoryDetailView
from products.views.product_view import ProductView

urlpatterns = [
    re_path(r'categories/?$', CategoryView.as_view()),
    re_path(r'categories/(?P<pk>\d+)/?$', CategoryDetailView.as_view()),
    re_path(r'products/?$', ProductView.as_view()),

]

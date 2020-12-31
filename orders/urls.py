from django.urls import re_path
from rest_framework.routers import DefaultRouter

from orders.views.order_item_view import OrderItemView
from orders.views.orders_view import OrderView


router = DefaultRouter()
router.register(r'order', OrderView, basename='order-url')


urlpatterns = [
    re_path(r'orders/?$', OrderItemView.as_view()),
#     # re_path(r'categories/(?P<pk>\d+)/?$', CategoryDetailView.as_view()),
#     # re_path(r'categories/(?P<pk>\d+)/products/?$', ProductView.as_view()),
#
        ]
urlpatterns += router.urls
from django.urls import path
from . import views

urlpatterns = [
    path(
        "orders/",
        views.my_orders,
        name="orders",
    ),

    path(
        "orders/<str:tracking_code>/",
        views.order_detail,
        name="order_detail",
    ),

    path(
        "orders/<str:tracking_code>/cancel/",
        views.cancel_order,
        name="cancel_order",
    ),
]
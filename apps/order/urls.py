from django.urls import path

from apps.order.views.order_views import OrderDetailAPIView, OrderListAPIView

# <<--------------------------------- Order URLs --------------------------------->>
urlpatterns = [
    path("", OrderListAPIView.as_view(), name="orders"),
    path("<int:pk>/", OrderDetailAPIView.as_view(), name="order_details"),
]

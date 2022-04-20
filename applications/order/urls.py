from django.urls import path

from applications.order.views import order, order_history

urlpatterns = [
    path('', order),
    path('history/', order_history)
    # path('history/', order_history)
]

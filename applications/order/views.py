from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from applications.order.serializers import OrderProductSerializer
from applications.product.models import Product


class OrderView(GenericViewSet, CreateModelMixin):
    queryset = Product.objects.all()
    serializer_class = OrderProductSerializer


# action --> likes
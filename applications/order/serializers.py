from rest_framework import serializers

from applications.order.models import *
from applications.product.models import Product


class OrderProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Order
        fields = '__all__'



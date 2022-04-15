from rest_framework import serializers

from applications.order.models import *
from applications.product.models import Product

#
# class OrderSerializers(serializers.ModelSerializer):
#     owner = serializers.ReadOnlyField(source='owner.email')    # это поле только для чтение(не обьязателньо заполнять)    || source='owner.email' = отображай email ownera
#     phone = serializers.CharField(max_length=30)
#
#     class Meta:
#         model = OrderItem
#         fields = ('product', )


class OrderProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')    # это поле только для чтение(не обьязателньо заполнять)    || source='owner.email' = отображай email ownera

    class Meta:
        model = Order
        fields = '__all__'



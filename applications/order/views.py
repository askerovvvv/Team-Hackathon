from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from applications.order.models import Order
from applications.order.sendmessage import sendTelegram
from applications.order.serializers import OrderProductSerializer
from applications.product.models import Product


class OrderView(GenericViewSet, CreateModelMixin):
    queryset = Product.objects.all()
    serializer_class = OrderProductSerializer


@api_view(['POST'])
def order(request):
    # print(dir(request.user))
    if request.user.is_authenticated:
        serializer = OrderProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            sendTelegram(request.data['phone'], request.data['name'])
            return Response("Ваша заявка принята!")
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    else:
        return Response("Войдите в систему")



@api_view(['GET'])
def order_history(request):
    print(request.user.order)
    if request.user.is_authenticated:
        order = request.user.order
        serializer = OrderProductSerializer(order, many=True)
        return Response(serializer.data)
    else:
        return Response("Войдите в систему")



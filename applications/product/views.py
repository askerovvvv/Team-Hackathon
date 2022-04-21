from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from applications.product.filters import ProductFilter
from applications.product.models import Product, ProductReview, Likes, ProductFavourites
from applications.product.serializers import ProductSerializer, ReviewSerializer, FavouritesSerializer


class LargeResultsSetPagination(PageNumberPagination):      # РЕКОМЕНДУЕТСЯ так называть класс если хотим переопределить пагинацию
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]  # локально указали чот будет фильтрация, поиск, ordering - группировка
    # filterset_fields = ['category', 'owner']    # указали по каким поля будем фильтровать
    filterset_class = ProductFilter     #  свой кастомный класс сделали
    ordering_fields = ['id', 'price']
    search_fields = ['name', 'description']

    ##Likes
    @action(methods=['POST'], detail=True)
    def like(self, request, pk): #http://localhost:8000/product/id_product/rating/
        obj = Likes.objects.filter(product=self.get_object(), owner=request.user)
        print('---------------')
        if obj:
            obj.delete()
            return Response('unliked')
        obj = Likes.objects.create(owner=request.user, product=self.get_object())
        obj.save()
        return Response('liked')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)   # при создании продукта нам не придется ввести кто owner так как будет автоматически залогинненого пользователя
        # переходим в serializers и настраиваем


class ProductReview(CreateAPIView):
    queryset = ProductReview.objects.all()
    serializer_class = ReviewSerializer


class ProductFavouritesApi(CreateAPIView):
    queryset = ProductFavourites.objects.all()
    serializer_class = FavouritesSerializer


@api_view(['GET'])
def product_favoruites(request):
    if request.user.is_authenticated:
        produ = request.user.favouriters
        serializer = FavouritesSerializer(produ, many=True)
        return Response(serializer.data)
    else:
        return Response("Войдите в систему")

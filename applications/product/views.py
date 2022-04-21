from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from applications.product.filters import ProductFilter
from applications.product.models import Product, ProductReview, Likes, ProductFavourites# Rating  # PhonesParser
from applications.product.serializers import ProductSerializer, ReviewSerializer, FavouritesSerializer
    #RatingSerializers
# from parser import main


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    ordering_fields = ['id', 'price']
    search_fields = ['name', 'description']


    def get_permissions(self):
        print(self.action)
        if self.action in ['list', 'retrieve']:
            permissions = []
        elif self.action == 'rating' or self.action == 'like':
            permissions = [IsAuthenticated]
        else:
            permissions = [IsAuthenticated]
        return [permission() for permission in permissions]


    ##Likes
    @action(methods=['POST'], detail=True)
    def like(self, request, pk):
        obj = Likes.objects.filter(product=self.get_object(), owner=request.user)
        print('---------------')
        if obj:
            obj.delete()
            return Response('unliked')
        obj = Likes.objects.create(owner=request.user, product=self.get_object())
        obj.save()
        return Response('liked')


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # @action(methods=['POST'], detail=True) # detail=True
    # def rating(self, request, pk):
    #     serializer = RatingSerializers(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     try:
    #         obj = Rating.objects.get(product=self.get_object(), owner=request.user)
    #         obj.rating = request.data['rating']
    #     except Rating.DoesNotExist:
    #         obj = Rating(owner=request.user, product=self.get_object(), rating=request.data['rating'])
    #
    #     obj.save()
    #     return Response(request.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProductReview(CreateAPIView):
    queryset = ProductReview.objects.all()
    serializer_class = ReviewSerializer


class ProductFavouritesApi(CreateAPIView):
    queryset = ProductFavourites.objects.all()
    serializer_class = FavouritesSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@api_view(['GET'])
def product_favoruites(request):
    if request.user.is_authenticated:
        produ = request.user.favouriters
        serializer = FavouritesSerializer(produ, many=True)
        return Response(serializer.data)
    else:
        return Response("Войдите в систему")



# class PhoneParser(ModelViewSet):
#     queryset = PhonesParser.objects.all()
#     serializer_class = ParserSerializer

    # def create_vacation_view(self, request):
    #     print('+++++++++++++++++++++++++++++++++++++++')
    #     vacations = main()
    #     print('---------------------------------------')
    #     print(vacations)
    #     title = vacations.get('title')
    #     price = vacations.get('price')
    #     image = vacations.get('image')
    #     PhonesParser.objects.create(title=title, price=price, image=image)


    # @action(methods=['POST'], detail=True)
    # def parser(self, request): #http://localhost:8000/product/id_product/rating/
    #     print('----------------------------')
    #     vacations = main()
    #     print('dddddddddddddddddddddddddd')
    #     print(vacations)
    #     title = vacations.get('title')
    #     price = vacations.get('price')
    #     image = vacations.get('image')
    #     obj = PhonesParser.objects.create(title=title, price=price, image=image)
    #     print('---------------')
    #     obj.save()
    #     return Response('liked')







# @api_view(['POST'])
# def parser(request):
#     print('+++++++++++++++++++++++++++++++++')
#     a = main()
#     serializer = ParserSerializer(data=a) # десерилизация для БД
#     print('-----------------------')
#     print(serializer)
#     if serializer.is_valid(): # все ли данные указали,все ли серилизовали; проверяет на правильность
#     # title = a.objects.get('title')
#         serializer.save() # записывает информацию в базу данных
#     return Response(serializer.data, status=status.HTTP_201_CREATED) # выводит созданную инФОРМАЦИЮ а так же статус
#     # else:
#     #     return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)











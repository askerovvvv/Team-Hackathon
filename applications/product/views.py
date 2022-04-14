from django.db.models import Q
from django.shortcuts import render
from django.template.context_processors import request
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import *
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin, UpdateModelMixin,RetrieveModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from applications.product.filters import ProductFilter
from applications.product.models import Product, Rating, category
from applications.product.permissions import IsAdmin, IsAutor
from applications.product.serializers import ProductSerializer, RatingSerializers, CategorySerializers
from rest_framework.viewsets import ModelViewSet, GenericViewSet


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100


    def qet_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search')
        if search:
            queryset=queryset.filter(Q(name__icontains=search) | Q(description__icontains=search))
        return queryset
class DeleteUpdateRetriveView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes =[IsAuthenticated]
    pagination_class = LargeResultsSetPagination
    permission_classes = [IsAutor]


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class =  LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filter_fields = ['category':'owner']
    filterset_class=ProductFilter
    ordering_field= ['id','price']
    search_field = ['name','description']

    def get_permissions(self):
        print(self.action)
        if self.action in ['list','retrieve']:
            permissions = []
        elif self.action == 'rating':
            permissions = [IsAuthenticated]
        else:
            permissions = [IsAuthenticated]
        return [permission() for permission in permissions]

class ProductViewSet(ListModelMixin, CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin, GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    @action(methods=['POST'],detail=True)
    def rating(self,request,pk):#http://localhost:8000/product/id_product/rating/
        serializer = RatingSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            obj = Rating.objects.get(product=self.get_object(), owner= request.user)
            obj.rating=request.data['rating']
        except Rating.DoesNotExist:
            obj= Rating(owner=request.user,product=self.get_object(),rating= request.data['rating'])
        obj.save()
        return Response(request.data,status=status.HTTP_201_CREATED)

class CategoryListCreateView(ListCreateAPIView):
    queryset = category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [IsAuthenticated]


class CategoryRetriveDeleteUpdateView(RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    queryset = category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [IsAuthenticated]
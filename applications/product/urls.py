from django.urls import path, include
from rest_framework.routers import DefaultRouter

from applications.product.views import *

router = DefaultRouter()
router.register('', ProductViewSet)
# router.register('', PhoneParser)
#

urlpatterns = [
    path('review/', ProductReview.as_view()),
    path('favourites/', ProductFavouritesApi.as_view()),
    path('get-favourites/', product_favoruites),
    # path('par/', parser),
    path('', include(router.urls)),         # он сам распределяет GET POST запросы весь CRUD |       нужно роутер в конце писать

]


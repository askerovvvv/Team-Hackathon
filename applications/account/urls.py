from django.urls import path

from applications.account.views import *

urlpatterns = [
    path('register/', RegisterApiView.as_view()),
    path('activate/<uuid:activation_code>/',ActivationApiView.as_view()),
    path('login/', LoginApiView.as_view()),
    path('custom/', custom)
]

from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

from applications.account.serializers import RegisterSerializer, LoginSerializer

User = get_user_model()


class RegisterApiView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            message = 'Вы успешно зарегистрированы. Вам отправлено письмо с активизацией'
            return Response(message, status=201)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ActivationApiView(APIView):
    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response("Вы успешно актвизировали ваш аккаунт", status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response("Активационный код не действителен")


class LoginApiView(ObtainAuthToken):
    serializer_class = LoginSerializer



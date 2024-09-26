from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json

from Users.models import UserProfileModel
from Users.serializers import UserProfileModelSerializer


class User_registration(APIView):
    def post(self, request):
        data = request.data
        print(data)
        serializer = UserProfileModelSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            print(serializer.errors)  # Логируем ошибки
            return Response(serializer.errors, status=400)

    def get(self, request):
        todos = UserProfileModel.objects.all()
        serializer = UserProfileModelSerializer(todos, many=True)
        return Response(serializer.data, status=200)



@method_decorator(csrf_exempt, name='dispatch')
class UserLoginAPI(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            # Аутентификация пользователя
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'Авторизация успешна', 'success': True}, status=200)
            else:
                return JsonResponse({'message': 'Неправильный логин или пароль', 'success': False}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Неверный формат данных'}, status=400)

# serializers.py
from django.contrib.auth import authenticate
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            # Проверяем пользователя через email и пароль
            user = authenticate(email=email, password=password)
            if user is None:
                raise serializers.ValidationError('Неверные учетные данные')
            data['user'] = user
        else:
            raise serializers.ValidationError('Необходимо указать email и пароль')
        return data

# serializers.py
from django.contrib.auth import authenticate
from rest_framework import serializers

from StoreHouse.models import Company
from .models import User


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
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



from rest_framework import serializers
from AuthReg.models import User

class UserDetailsSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField(source="company.name")

    class Meta:
        model = User
        fields = ['id', 'name', 'surname', 'patronymic', 'email', 'company']

    def get_company(self, obj):
        # Проверяем, есть ли у пользователя компания
        return obj.company.name if obj.company else None


class CompanyDetailsSerializer(serializers.ModelSerializer):
    admin_surname = serializers.SerializerMethodField()
    admin_name = serializers.SerializerMethodField()
    admin_patronymic = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['name', 'admin_surname', 'admin_name', 'admin_patronymic']

    def get_admin_surname(self, obj):
        admin = obj.employees.filter(is_company_admin=True).first()
        return admin.surname if admin else "Не указано"

    def get_admin_name(self, obj):
        admin = obj.employees.filter(is_company_admin=True).first()
        return admin.name if admin else "Не указано"

    def get_admin_patronymic(self, obj):
        admin = obj.employees.filter(is_company_admin=True).first()
        return admin.patronymic if admin else "Не указано"

from rest_framework import serializers
from .models import InventoryRequest, Warehouse

class InventoryRequestSerializer(serializers.ModelSerializer):

    deadline = serializers.DateTimeField(format="%d.%m.%Y %H:%M")  # Настройка формата времени

    # Используем SlugRelatedField для сериализации названий складов
    warehouses = serializers.SlugRelatedField(
        many=True,  # Для обработки списка складов
        slug_field='name',  # Поле 'name' будет использоваться для представления склада
        queryset=Warehouse.objects.all()  # Запрос для поиска складов по названиям
    )

    class Meta:
        model = InventoryRequest
        fields = ['employee', 'warehouses', 'deadline', 'status']  # Добавляем нужные поля

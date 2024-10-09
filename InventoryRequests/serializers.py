from rest_framework import serializers
from .models import InventoryRequest, Warehouse


class InventoryRequestSerializer(serializers.ModelSerializer):
    deadline = serializers.DateTimeField(format="%d.%m.%Y %H:%M")  # Настройка формата времени

    # Сериализация списка складов
    warehouses = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Warehouse.objects.all()
    )
    class Meta:
        model = InventoryRequest
        fields = ['employee', 'warehouses', 'deadline', 'status']

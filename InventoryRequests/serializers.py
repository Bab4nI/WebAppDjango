from rest_framework import serializers
from .models import InventoryRequest, Warehouse, Item

class InventoryRequestSerializer(serializers.ModelSerializer):
    items = serializers.SlugRelatedField(
        many=True,
        slug_field='serial_number',
        queryset=Item.objects.all(),
        required=False
    )

    warehouses = serializers.SlugRelatedField(
        many=True,
        slug_field='name',  # Возвращаем имя склада
        queryset=Warehouse.objects.all(),
        required=True
    )

    class Meta:
        model = InventoryRequest
        fields = ['id', 'employee', 'warehouses', 'items', 'deadline', 'status']

class ItemSerializer(serializers.ModelSerializer):
    warehouse = serializers.CharField(source='warehouse.name')  # Возвращаем имя склада вместо ID

    class Meta:
        model = Item
        fields = ['id', 'name', 'serial_number', 'warehouse']  # Укажите нужные поля
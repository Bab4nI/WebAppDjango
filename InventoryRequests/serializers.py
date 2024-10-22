from rest_framework import serializers
from .models import InventoryRequest, Warehouse, Item


class InventoryRequestSerializer(serializers.ModelSerializer):
    items = serializers.SlugRelatedField(
        many=True,
        slug_field='serial_number',
        queryset=Item.objects.all(),
        required=False  # Делаем необязательным
    )

    # Поле для складов (с числовыми ID)
    warehouses = serializers.SlugRelatedField(
        many=True,
        slug_field='name',  # Если хотите использовать имена складов вместо ID
        queryset=Warehouse.objects.all(),
        required=True
    )

    class Meta:
        model = InventoryRequest
        fields = ['id', 'employee', 'warehouses', 'items', 'deadline', 'status']



from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'serial_number', 'warehouse']  # Укажите нужные поля

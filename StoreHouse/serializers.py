from .models import Warehouse
from rest_framework import serializers
from StoreHouse.models import Item
from AuthReg.models import User

class ItemSerializer(serializers.ModelSerializer):
    company = serializers.CharField(source='company.name')  # Вернуть название компании
    warehouse = serializers.CharField(source='warehouse.name')  # Вернуть название склада

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'serial_number', 'company', 'warehouse']
# serializers.py

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'name']

class ItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['serial_number', 'warehouse']

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Подставь свою модель
        fields = ['id', 'name', 'surname', 'patronymic', 'email']



from .models import Warehouse
from rest_framework import serializers
from StoreHouse.models import Item
from AuthReg.models import User

class ItemSerializer(serializers.ModelSerializer):
    qr_code_url = serializers.SerializerMethodField()
    company = serializers.CharField(source='company.name')  # Вернуть название компании
    warehouse = serializers.CharField(source='warehouse.name')  # Вернуть название склада

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'serial_number', 'company', 'warehouse']

    def get_qr_code_url(self, obj):
        request = self.context.get('request')
        if obj.qr_code:
            return request.build_absolute_uri(obj.qr_code.url)
        return None

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



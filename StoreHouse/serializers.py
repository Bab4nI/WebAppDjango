from .models import Warehouse
from rest_framework import serializers
from StoreHouse.models import Item
from AuthReg.models import User

class ItemSerializer(serializers.ModelSerializer):
    company = serializers.CharField(source='company.name')  # Вернуть название компании
    warehouse = serializers.CharField(source='warehouse.name')  # Вернуть название склада

    qr_code_url = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = '__all__'

    def get_qr_code_url(self, obj):
        request = self.context.get('request', None)
        if request is not None and obj.qr_code:
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
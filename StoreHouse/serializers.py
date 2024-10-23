from rest_framework import serializers
from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    qr_code_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Item
        fields = '__all__'

    def get_qr_code_url(self, obj):
        request = self.context.get('request')
        if obj.qr_code:
            return request.build_absolute_uri(obj.qr_code.url)
        return None

class ItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['serial_number', 'warehouse']  # Теперь обновляем только склад

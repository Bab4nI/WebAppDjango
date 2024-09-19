from django import forms
from .models import Warehouse, Item

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['name']

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'serial_number', 'warehouse']
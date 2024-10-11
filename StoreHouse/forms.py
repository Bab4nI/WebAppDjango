from django import forms
from .models import Warehouse, Item, ItemMovement

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['name']

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'warehouse']

class ItemMovementForm(forms.ModelForm):
    class Meta:
        model = ItemMovement
        fields = ['item', 'to_warehouse', 'new_description']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['to_warehouse'].queryset = Warehouse.objects.filter(company=user.company)
        
        if user:
            self.fields['item'].queryset = Item.objects.filter(warehouse__company=user.company)

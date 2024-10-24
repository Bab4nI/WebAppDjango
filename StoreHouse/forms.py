from django import forms
from .models import Warehouse, Item, ItemMovement

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['name', 'parent_warehouse']
        
    def __init__(self, *args, **kwargs):
        parent_warehouse = kwargs.pop('parent_warehouse', None)  # Извлекаем переданный склад
        super(WarehouseForm, self).__init__(*args, **kwargs)

        if parent_warehouse:
            # Фильтруем поле 'warehouse', чтобы показывать только подсклады данного родительского склада
            self.fields['parent_warehouse'].queryset = Warehouse.objects.filter(parent_warehouse=parent_warehouse)
        else:
            self.fields['parent_warehouse'].queryset = Warehouse.objects.all()  # Если нет подскладов

            
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'warehouse', 'responsible_employee']

    def __init__(self, *args, **kwargs):
        parent_warehouse = kwargs.pop('parent_warehouse', None)  # Извлекаем переданный склад
        super(ItemForm, self).__init__(*args, **kwargs)

        if parent_warehouse:
            # Ограничиваем выбор складов только подскладами выбранного склада
            self.fields['warehouse'].queryset = Warehouse.objects.filter(parent_warehouse=parent_warehouse)
        else:
            # Если склад не передан, можно оставить стандартный выбор
            self.fields['warehouse'].queryset = Warehouse.objects.all()

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

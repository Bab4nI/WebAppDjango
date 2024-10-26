from django import forms
from .models import InventoryRequest

class InventoryRequestForm(forms.ModelForm):
    class Meta:
        model = InventoryRequest
        fields = ['employee', 'warehouses', 'deadline', 'status']  # Use 'warehouses' here
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'})  # Шаблон даты
        }
    def __init__(self, *args, **kwargs):
        super(InventoryRequestForm, self).__init__(*args, **kwargs)
        self.fields['status'].choices = [('pending', 'Не проведена'), ('completed', 'Проведена')]



    
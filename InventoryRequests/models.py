# from django.db import models
# from StoreHouse.models import Warehouse
# from AuthReg.models import User  # Directly import User

# class InventoryRequest(models.Model):
#     employee = models.ForeignKey(User, on_delete=models.CASCADE)  # Refer to User model directly
#     warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)  # Refer to Warehouse model directly
#     deadline = models.DateField()
#     status = models.CharField(max_length=50, choices=[('pending', 'Не проведена'), ('completed', 'Проведена')])

#     def __str__(self):
#         return f"{self.employee} - {self.warehouse} - {self.status}"

from django.db import models
from StoreHouse.models import Item, Warehouse

class InventoryRequest(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Не проведена'),
        ('completed', 'Проведена'),
    ]

    employee = models.CharField(max_length=200)
    warehouses = models.ManyToManyField(Warehouse)
    items = models.ManyToManyField(Item, related_name='requests')  # Основные предметы в заявке
    missing_items = models.ManyToManyField(Item, related_name='missing_in_requests', blank=True)  # Отсутствующие предметы
    extra_items = models.ManyToManyField(Item, related_name='extra_in_requests', blank=True)  # Лишние предметы
    deadline = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def str(self):
        return f"Заявка от {self.employee} - Статус: {self.get_status_display()}"
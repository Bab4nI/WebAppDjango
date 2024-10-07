from django.db import models
from StoreHouse.models import Warehouse

class InventoryRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Не проведена'),
        ('completed', 'Проведена'),
    ]

    employee = models.CharField(max_length=200)
    warehouses = models.ManyToManyField(Warehouse)
    deadline = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Заявка от {self.employee} - Статус: {self.get_status_display()}"


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

    def __str__(self):
        return f"Заявка от {self.employee} - Статус: {self.get_status_display()}"

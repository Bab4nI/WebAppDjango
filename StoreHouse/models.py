from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Warehouse(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='warehouses')
    parent_warehouse = models.ForeignKey('self', on_delete=models.CASCADE, related_name='warehouses', null = True, blank = True)
    name = models.CharField(max_length=200)
    fullness = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    @property
    def is_root(self):
        """Проверка, является ли склад корневым"""
        return self.parent_warehouse is None
        
class Item(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='items')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    serial_number = models.CharField(max_length=100, unique=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return f"{self.name} (Серийный номер: {self.serial_number})"


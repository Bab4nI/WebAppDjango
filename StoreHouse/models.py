from django.db import models

class Warehouse(models.Model):
    name = models.CharField(max_length=200)
    fullness = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    serial_number = models.CharField(max_length=100, unique=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='items')  # related_name корректен здесь
    location = models.CharField(max_length=200, null=True)
    assigned_to = models.CharField(max_length=200, null=True)
    registration_date = models.DateField(null=True)
    def __str__(self):
        return f"{self.name} (Серийный номер: {self.serial_number})"


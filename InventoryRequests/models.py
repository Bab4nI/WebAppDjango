from django.db import models
from StoreHouse.models import Warehouse
from AuthReg.models import User  # Directly import User

class InventoryRequest(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)  # Refer to User model directly
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)  # Refer to Warehouse model directly
    deadline = models.DateField()
    status = models.CharField(max_length=50, choices=[('pending', 'Не проведена'), ('completed', 'Проведена')])

    def __str__(self):
        return f"{self.employee} - {self.warehouse} - {self.status}"

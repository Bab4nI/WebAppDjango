import qrcode
from django.core.files import File
from io import BytesIO
from django.conf import settings
from django.core.files.base import ContentFile #Для QR

from django.db import models
from .utils import *
from django.contrib.auth import get_user_model

class Company(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name


class Warehouse(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='warehouses')
    parent_warehouse = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub_warehouses', null = True, blank = True)
    name = models.CharField(max_length=200)

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
    serial_number = models.CharField(max_length=100, unique=True, editable=False)
    responsible_employee = models.ForeignKey('AuthReg.User', on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True) 

    def generate_serial_number(self):
        if not self.warehouse or not self.warehouse.company:
            raise ValueError("Warehouse or company is not set")
        data =  f"{self.warehouse.company.id:04d}-{self.warehouse.id:04d}-{self.id:06d}"
        return encrypt_data(data)

    def generate_qr_code(self, serial_number):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(serial_number)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buf = BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)

        filename = f'qr_code_{self.serial_number}.png'
        self.qr_code.save(filename, ContentFile(buf.read()), save=False) 
        buf.close()

    def save(self, *args, **kwargs):
        if not self.id:
            super(Item, self).save(*args, **kwargs) 

        if not self.serial_number:
            self.serial_number = self.generate_serial_number()

        self.generate_qr_code(self.serial_number)

        super(Item, self).save(*args, **kwargs) 
    def __str__(self):
        return f"{self.name} (Серийный номер: {self.serial_number})"
    
class ItemMovement(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="movements")
    from_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="moved_from")
    to_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="moved_to")
    timestamp = models.DateTimeField(auto_now_add=True)
    new_description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE) 
    

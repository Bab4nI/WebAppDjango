import qrcode
from django.core.files import File
from io import BytesIO
from django.conf import settings
from django.core.files.base import ContentFile #Для QR
from django.utils import timezone
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
        # Определяем, новый ли это объект
        is_new = self.pk is None

        # Первое сохранение, если объект новый, чтобы получить ID
        if is_new:
            super(Item, self).save(*args, **kwargs)  # Первое сохранение

            # Записываем событие создания в историю
            ItemHistory.objects.create(
                company = self.company,
                item_name=str(self.name),
                warehouse_name = str(self.warehouse.name),
                responsible_employee_surname = str(self.responsible_employee.surname),
                responsible_employee_name = str(self.responsible_employee.name),
                responsible_employee_email = str(self.responsible_employee.email),
                action_type='created',  # Указываем, что это удаление
                field_name="Создано",
                old_value=str(self),  # Сохраняем текущее состояние объекта перед удалением
            new_value=None,  # После удаления объекта уже нет
            )

        # Генерируем серийный номер, если он еще не создан
        if not self.serial_number:
            self.serial_number = self.generate_serial_number()

        # Генерация QR-кода, если серийный номер был создан
        if self.serial_number:
            self.generate_qr_code(self.serial_number)

        # Проверяем изменения только если объект уже существует
        if not is_new:
            # Получаем старое состояние объекта из базы данных перед изменением
            old_item = Item.objects.get(pk=self.pk)
            # Проверяем, изменилось ли хотя бы одно поле
            has_changes = False

            for field in self._meta.fields:
                field_name = field.name
                old_value = getattr(old_item, field_name)
                new_value = getattr(self, field_name)

                # Если хотя бы одно поле изменилось, отмечаем это
                if old_value != new_value:
                    has_changes = True
                    break  # Выходим из цикла, как только нашли изменения

            # Если есть изменения, сохраняем запись в историю
            if has_changes:
                ItemHistory.objects.create(
                    company = self.company,
                    item_name=str(self.name),
                    warehouse_name = str(self.warehouse.name),
                    responsible_employee_surname = str(self.responsible_employee.surname),
                    responsible_employee_name = str(self.responsible_employee.name),
                    responsible_employee_email = str(self.responsible_employee.email),
                    action_type='changed',  # Указываем, что это удаление
                    field_name="Изменено",
                    old_value=str(self),  # Сохраняем текущее состояние объекта перед удалением
                    new_value=None,  # После удаления объекта уже нет
                )

        # Сохраняем объект после всех изменений
        super(Item, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Перед удалением объекта записываем событие удаления в историю
        ItemHistory.objects.create(
            company = self.company,
            item_name=str(self.name),
            warehouse_name = str(self.warehouse.name),
            responsible_employee_surname = str(self.responsible_employee.surname),
            responsible_employee_name = str(self.responsible_employee.name),
            responsible_employee_email = str(self.responsible_employee.email),
            action_type='deleted',  # Указываем, что это удаление
            field_name="Удалено",
            old_value=str(self),  # Сохраняем текущее состояние объекта перед удалением
            new_value=None,  # После удаления объекта уже нет
        )

        # Затем выполняем реальное удаление объекта
        super(Item, self).delete(*args, **kwargs)


    def __str__(self):
        return f"{self.name} (Серийный номер: {self.serial_number})"
    
    
class ItemHistory(models.Model):
    ACTION_CHOICES = [
        ('created', 'Создано'),
        ('updated', 'Изменено'),
        ('deleted', 'Удалено'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='actions')
    item_name = models.CharField(max_length=200)
    warehouse_name = models.CharField(max_length=200)
    responsible_employee_surname = models.CharField(max_length=200)
    responsible_employee_name = models.CharField(max_length=200)
    responsible_employee_email = models.CharField(max_length=200)
    field_name = models.CharField(max_length=200, null=True, blank=True)
    old_value = models.TextField(null=True, blank=True)
    new_value = models.TextField(null=True, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    # Новое поле для хранения типа действия (создание, изменение, удаление)
    action_type = models.CharField(max_length=10, choices=ACTION_CHOICES, default='updated')

    def __str__(self):
        return f"{self.get_action_type_display()} — {self.item} ({self.changed_at})"
    

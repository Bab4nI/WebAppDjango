# Generated by Django 5.1.1 on 2024-10-25 15:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InventoryRequests', '0001_initial'),
        ('StoreHouse', '0008_itemhistory_warehouse_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventoryrequest',
            name='warehouses',
        ),
        migrations.AddField(
            model_name='inventoryrequest',
            name='warehouse',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='StoreHouse.warehouse'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='inventoryrequest',
            name='deadline',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='inventoryrequest',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='inventoryrequest',
            name='status',
            field=models.CharField(choices=[('pending', 'Не проведена'), ('completed', 'Проведена')], max_length=50),
        ),
    ]
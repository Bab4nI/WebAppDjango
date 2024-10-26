# Generated by Django 5.1.1 on 2024-10-26 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InventoryRequests', '0002_remove_inventoryrequest_warehouses_and_more'),
        ('StoreHouse', '0008_itemhistory_warehouse_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryrequest',
            name='extra_items',
            field=models.ManyToManyField(blank=True, related_name='extra_in_requests', to='StoreHouse.item'),
        ),
        migrations.AddField(
            model_name='inventoryrequest',
            name='items',
            field=models.ManyToManyField(related_name='requests', to='StoreHouse.item'),
        ),
        migrations.AddField(
            model_name='inventoryrequest',
            name='missing_items',
            field=models.ManyToManyField(blank=True, related_name='missing_in_requests', to='StoreHouse.item'),
        ),
        migrations.AlterField(
            model_name='inventoryrequest',
            name='deadline',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='inventoryrequest',
            name='employee',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='inventoryrequest',
            name='status',
            field=models.CharField(choices=[('pending', 'Не проведена'), ('completed', 'Проведена')], default='pending', max_length=10),
        ),
        migrations.RemoveField(
            model_name='inventoryrequest',
            name='warehouse',
        ),
        migrations.AddField(
            model_name='inventoryrequest',
            name='warehouse',
            field=models.ManyToManyField(to='StoreHouse.warehouse'),
        ),
    ]
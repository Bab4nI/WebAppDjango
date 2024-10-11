# Generated by Django 5.1.1 on 2024-10-10 14:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StoreHouse', '0005_remove_warehouse_fullness_alter_item_serial_number'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='warehouse',
            name='parent_warehouse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_warehouses', to='StoreHouse.warehouse'),
        ),
        migrations.CreateModel(
            name='ItemMovement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('new_description', models.TextField(blank=True, null=True)),
                ('from_warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moved_from', to='StoreHouse.warehouse')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movements', to='StoreHouse.item')),
                ('to_warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moved_to', to='StoreHouse.warehouse')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

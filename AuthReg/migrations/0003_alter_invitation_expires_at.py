# Generated by Django 5.1.1 on 2024-10-23 09:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthReg', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 30, 9, 44, 13, 690685, tzinfo=datetime.timezone.utc)),
        ),
    ]

# Generated by Django 5.1.1 on 2024-10-23 20:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthReg', '0005_alter_invitation_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 30, 20, 37, 47, 806685, tzinfo=datetime.timezone.utc)),
        ),
    ]

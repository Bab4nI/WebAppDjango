# Generated by Django 5.1.1 on 2024-10-06 15:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthReg', '0014_alter_invitation_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 13, 15, 29, 2, 852212, tzinfo=datetime.timezone.utc)),
        ),
    ]

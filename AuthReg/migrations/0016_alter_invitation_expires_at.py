# Generated by Django 5.1.1 on 2024-10-24 18:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthReg', '0015_alter_invitation_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 31, 18, 24, 42, 310868, tzinfo=datetime.timezone.utc)),
        ),
    ]

# Generated by Django 5.1.1 on 2024-10-07 23:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthReg', '0024_alter_invitation_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 14, 23, 23, 34, 426818, tzinfo=datetime.timezone.utc)),
        ),
    ]

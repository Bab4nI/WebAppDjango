# Generated by Django 5.1.1 on 2024-10-09 10:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthReg', '0041_alter_invitation_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 16, 10, 20, 53, 821025, tzinfo=datetime.timezone.utc)),
        ),
    ]

# Generated by Django 5.1.1 on 2024-10-06 14:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthReg', '0010_alter_invitation_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 13, 14, 56, 25, 517187, tzinfo=datetime.timezone.utc)),
        ),
    ]

# Generated by Django 5.1.1 on 2024-10-10 06:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthReg', '0019_alter_invitation_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 17, 6, 48, 52, 68347, tzinfo=datetime.timezone.utc)),
        ),
    ]

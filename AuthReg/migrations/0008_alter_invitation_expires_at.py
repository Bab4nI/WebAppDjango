# Generated by Django 5.1.1 on 2024-10-03 18:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthReg', '0007_alter_invitation_expires_at_alter_user_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 10, 18, 54, 20, 705181, tzinfo=datetime.timezone.utc)),
        ),
    ]

# Generated by Django 5.1.1 on 2024-10-03 19:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthReg', '0009_remove_user_first_name_remove_user_last_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 10, 19, 0, 15, 126686, tzinfo=datetime.timezone.utc)),
        ),
    ]
# Generated by Django 5.1.1 on 2024-09-27 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0005_userprofilemodel_password'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfileModel',
        ),
    ]

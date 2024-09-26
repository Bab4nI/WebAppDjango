from django.db import models


class UserProfileModel(models.Model):
    last_name = models.TextField(max_length=100, default='Не указано', verbose_name='Фамилия')
    first_name = models.TextField(max_length=100, default='Не указано', verbose_name='Имя')
    middle_name = models.TextField(max_length=100, blank=True, null=True, default='Не указано', verbose_name='Отчество')
    email = models.TextField(max_length=100, blank=True, null=True, verbose_name='Адрес электронной почты')
    phone_number = models.TextField(max_length=20, default='Не указано', verbose_name='Номер телефона')
    password = models.TextField(max_length=20, default='Не указано', verbose_name='Пароль')
    role = models.TextField(max_length=20, default='employee', verbose_name='Роль')

from django.db import models
from django.contrib.auth.models import AbstractUser
from WebAppDjango.managers import UserManager

class User(AbstractUser):
   username = None

   is_admin = models.BooleanField('Is admin', default=False)
   is_employee = models.BooleanField('Is employee', default=False)
   patronymic = models.CharField('Отчество', max_length=30, blank=True, null=True)
   surname = models.CharField('Фамилия', max_length=30, blank=False, null=True)
   name = models.CharField('Имя', max_length=30, blank=False, null=True)
   email = models.EmailField('Электронная почта', unique=True)
   USERNAME_FIELD = 'email'
   REQUIRED_FIELDS = []

   objects = UserManager()

   def __str__(self):
      return self.email




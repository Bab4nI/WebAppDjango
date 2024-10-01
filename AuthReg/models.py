from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
   is_admin = models.BooleanField('Is admin', default=False)
   is_employee = models.BooleanField('Is employee', default=False)



import uuid
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from WebAppDjango.managers import UserManager
from StoreHouse.models import Company

def get_expiration_date():
    return timezone.now() + timezone.timedelta(days=7)

class Invitation(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="invitations")
    email = models.EmailField()
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=get_expiration_date())
    role = models.CharField(max_length=50, choices=(('admin', 'Админ'), ('employee', 'Сотрудник')))
    used = models.BooleanField(default=False)

    def is_valid(self):
        return not self.used and self.expires_at > timezone.now()
    
class User(AbstractUser):
   username = None
   first_name = None
   last_name = None

   company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name='employees')
   is_company_admin = models.BooleanField(default=False)
   patronymic = models.CharField('Отчество', max_length=30, blank=True, null=True)
   surname = models.CharField('Фамилия', max_length=30, blank=False, null=True)
   name = models.CharField('Имя', max_length=30, blank=False, null=True)
   email = models.EmailField('Электронная почта', unique=True)
   USERNAME_FIELD = 'email'
   REQUIRED_FIELDS = []

   objects = UserManager()

   def __str__(self):
      return f"{self.surname} {self.name} {self.patronymic} : {self.email}"




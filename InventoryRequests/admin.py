from django.contrib import admin
from .models import InventoryRequest

class InventoryRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'deadline', 'status')
    list_filter = ('status',)

admin.site.register(InventoryRequest, InventoryRequestAdmin)

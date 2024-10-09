from django.urls import path

from . import views
from .views import ItemBySerialNumber, UpdateItemLocation

app_name = "StoreHouse"

urlpatterns = [
    path('create_warehouse/', views.create_warehouse, name='create_warehouse'),
    path('create_item', views.create_item, name = 'create_item'),
    path('warehouses/', views.warehouse_list, name='warehouse_list'),
    path('items/', views.item_list, name='item_list'),
    path('item/<int:item_id>/delete/', views.delete_item, name='delete_item'),
    path('inventory/', views.inventory, name = 'inventory'),
]
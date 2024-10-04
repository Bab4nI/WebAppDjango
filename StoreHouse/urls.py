from django.urls import path

from . import views
from .views import ItemBySerialNumber, UpdateItemLocation

app_name = "StoreHouse"

urlpatterns = [
    path('create_warehouse/', views.create_warehouse, name='create_warehouse'),
    path('create_item', views.create_item, name = 'create_item'),
    path('warehouses/', views.warehouse_list, name='warehouse_list'),
    path('items/', views.item_list, name='item_list'),
    path('profile/', views.profile, name='profile'),
    path('items/<serial_number>/', ItemBySerialNumber.as_view(), name='item_by_serial'),
    path('itemsUpdate/<str:serial_number>/location/', UpdateItemLocation.as_view(), name='update_item_location'),
]
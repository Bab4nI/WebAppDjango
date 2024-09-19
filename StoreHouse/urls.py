from django.urls import path

from . import views

app_name = "StoreHouse"

urlpatterns = [
    path('create_warehouse/', views.create_warehouse, name='create_warehouse'),
    path('create_item', views.create_item, name = 'create_item'),
    path('warehouses/', views.warehouse_list, name='warehouse_list'),
    path('items/', views.item_list, name='item_list'),
    path('profile/', views.profile, name='profile'),
]
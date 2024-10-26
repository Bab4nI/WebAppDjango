from django.urls import path

from . import views
from .views import UpdateItemWarehouse, WarehouseListView, StockSearchView

app_name = "StoreHouse"

urlpatterns = [
    path('create_warehouse/', views.create_warehouse, name='create_warehouse'),
    path('search/', StockSearchView.as_view(), name='search-api'),
    path('create_item', views.create_item, name = 'create_item'),
    path('warehouse/<int:warehouse_id>/create', views.create_warehouse, name='create_warehouse'),
    path('warehouse/<int:warehouse_id>/delete/', views.delete_warehouse, name='delete_warehouse'),
    path('warehouse/<int:warehouse_id>/<int:warehouse_to_edit>/change/', views.edit_warehouse, name='edit_warehouse'),
    path('item/<int:warehouse_id>/create/', views.create_item, name = 'create_item'),
    path('item/<int:item_id>/delete/', views.delete_item, name='delete_item'),
    path('item/<int:warehouse_id>/<int:item_id>/edit/', views.edit_item, name='edit_item'),
    path('inventory/', views.inventory, name = 'inventory'),
    path('inventory/<int:warehouse_id>/', views.inventory, name='inventory_by_warehouse'),
    path('items/<str:serial_number>/', views.ItemBySerialNumber.as_view()),
    path('items/<str:serial_number>/update-warehouse/', UpdateItemWarehouse.as_view(),name='update_item_warehouse'),
    path('warehouses/', WarehouseListView.as_view(), name='warehouse-list'),
    path('action_log/', views.action_log,name='action_log'),
]
from django.urls import path
from .views import InventoryRequestListCreateView

urlpatterns = [
    path('inventory-requests/', InventoryRequestListCreateView.as_view(), name='inventory-requests-list-create'),
]

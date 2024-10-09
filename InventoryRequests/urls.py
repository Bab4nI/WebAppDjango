from django.urls import path
from .views import InventoryRequestView

urlpatterns = [
    path('inventory-requests/', InventoryRequestView.as_view(), name='inventory-requests-list-create'),
]

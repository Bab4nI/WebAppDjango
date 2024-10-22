from django.urls import path
from .views import InventoryRequestView, InventoryRequestPDFView, CompleteInventoryView, InventoryRequestItemsView

urlpatterns = [
    path('inventory-requests/', InventoryRequestView.as_view(), name='inventory-request-list'),
    path('inventory-requests/<int:request_id>/', InventoryRequestView.as_view(), name='inventory-request-detail'),
    path('inventory-requests/<int:request_id>/pdf/', InventoryRequestPDFView.as_view(), name='inventory-request-pdf'),
    path('inventory-requests/<int:request_id>/complete/', CompleteInventoryView.as_view(), name='complete_inventory'),
    path('inventory-requests/<int:request_id>/items/', InventoryRequestItemsView.as_view(), name='warehouse-items'),

]

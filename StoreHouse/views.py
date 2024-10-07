from django.shortcuts import render, redirect
from .forms import WarehouseForm, ItemForm
from .models import Warehouse, Item
from django.contrib.auth import decorators
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ItemSerializer, ItemUpdateSerializer  # Убрали Location


@decorators.login_required
def profile(request):
    return render(request, 'StoreHouse/profile.html')


def warehouse_list(request):
    warehouses = Warehouse.objects.all()
    return render(request, 'StoreHouse/warehouse_list.html', {'warehouses': warehouses})


def item_list(request):
    items = Item.objects.all()
    return render(request, 'StoreHouse/item_list.html', {'items': items})


def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            warehouse = item.warehouse
            warehouse.fullness += 1
            warehouse.save()
            return redirect('StoreHouse:item_list')
    else:
        form = ItemForm()
    return render(request, 'StoreHouse/create_item.html', {'form': form})


def create_warehouse(request):
    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('StoreHouse:warehouse_list')
    else:
        form = WarehouseForm()
    return render(request, 'StoreHouse/create_warehouse.html', {'form': form})


class ItemBySerialNumber(APIView):
    def get(self, request, serial_number):
        try:
            item = Item.objects.get(serial_number=serial_number)
            serializer = ItemSerializer(item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Item.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)


class UpdateItemWarehouse(APIView):  # Изменено название
    def patch(self, request, serial_number):
        try:
            item = Item.objects.get(serial_number=serial_number)
        except Item.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ItemUpdateSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

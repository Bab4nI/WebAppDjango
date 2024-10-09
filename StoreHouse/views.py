from django.shortcuts import render, redirect, get_object_or_404
from .forms import WarehouseForm, ItemForm
from .models import Warehouse
from django.contrib.auth import decorators
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Item
from .serializers import ItemSerializer, ItemUpdateSerializer


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
            item = form.save(commit = False)
            warehouse = item.warehouse
            warehouse.fullness += 1
            warehouse.save()
            return redirect('StoreHouse:item_list')
    else:
        form = ItemForm()
    return render(request, 'StoreHouse/create_item.html', {'form': form})

# def delete_item(request, item_id):
#     item = get_object_or_404(Item, id = item_id, warehouse__company=request.user.company)

#     if request.method == 'POST':
#         item.delete()
#         return redirect('item')

def create_warehouse(request):
    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('StoreHouse:warehouse_list')
    else:
        form = WarehouseForm()
    return render(request, 'StoreHouse/create_warehouse.html', {'form' : form})




class ItemBySerialNumber(APIView):
    def get(self, request, serial_number):
        try:
            # Ищем элемент по серийному номеру
            item = Item.objects.get(serial_number=serial_number)
            serializer = ItemSerializer(item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Item.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

class UpdateItemLocation(APIView):
    def patch(self, request, serial_number):
        try:
            # Ищем объект по серийному номеру
            item = Item.objects.get(serial_number=serial_number)
        except Item.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        # Передаем только данные для обновления местоположения
        serializer = ItemUpdateSerializer(item, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




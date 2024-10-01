from django.shortcuts import render, redirect
from .forms import WarehouseForm, ItemForm
from .models import Warehouse, Item

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

def create_warehouse(request):
    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('StoreHouse:warehouse_list')
    else:
        form = WarehouseForm()
    return render(request, 'StoreHouse/create_warehouse.html', {'form' : form})
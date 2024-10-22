from django.shortcuts import render, redirect, get_object_or_404

from AuthReg.models import User
from .forms import WarehouseForm, ItemForm, ItemMovementForm
from rest_framework import status
from .models import Item, ItemMovement
from .serializers import ItemUpdateSerializer
from django.urls import reverse
from .models import Warehouse
from .serializers import WarehouseSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .serializers import ItemSerializer, EmployeeSerializer  # Подставь свои сериализаторы



class SearchAPIView(APIView):

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q', None)

        if query is None or query == "":
            return Response({"error": "Поисковый запрос не указан"}, status=400)

        # Фильтрация по сотрудникам (например, по имени, фамилии и отчеству)
        employee_results = User.objects.filter(
            Q(name__icontains=query) | Q(surname__icontains=query) | Q(patronymic__icontains=query)
        )

        # Фильтрация по товарам (по названию товара)
        item_results = Item.objects.filter(name__icontains=query)

        # Сериализация данных
        employee_serializer = EmployeeSerializer(employee_results, many=True)
        item_serializer = ItemSerializer(item_results, many=True)

        # Объединение данных
        results = {
            "employees": employee_serializer.data,
            "items": item_serializer.data
        }

        return Response(results, status=200)


class WarehouseListView(APIView):
    def get(self, request):
        warehouses = Warehouse.objects.all()
        serializer = WarehouseSerializer(warehouses, many=True)
        return Response(serializer.data)

def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit = False)
            item.serial_number = item.generate_serial_number()
            item.save()
            return redirect('StoreHouse:item_list')
    else:
        form = ItemForm()
    return render(request, 'StoreHouse/create_item.html', {'form': form})

def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id, company=request.user.company)
    if request.method == 'POST':
        item.delete()
        return redirect('StoreHouse:item_list')  # Перенаправляем на список предметов
    return render(request, 'StoreHouse/confirm_delete.html', {'item': item})

def create_warehouse(request):
    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('StoreHouse:warehouse_list'))
    else:
        form = WarehouseForm()
    return render(request, 'StoreHouse/create_warehouse.html', {'form' : form})

def delete_warehouse(request, warehouse_id):
    warehouse = get_object_or_404(Warehouse, id=warehouse_id, company=request.user.company)
    if request.method == 'POST':
        warehouse.delete()
        return redirect(reverse('AuthReg:account'))

    return render(request, 'StoreHouse/confirm_delete_warehouse.html', {'warehouse': warehouse})

def inventory(request):
    if request.user.is_authenticated:
        user = request.user
        company = user.company

        if company:
            employees = company.employees.all()
            warehouses = company.warehouses.all()
            items = company.items.all()
            context = {
                'company': company,
                'employees': employees,
                'warehouses': warehouses,
                'items': items,
            }
        else:
            context = {
                'company': None,
                'employees': [],
                'warehouses': [],
                'items': [],
            }

        return render(request, 'StoreHouse/inventar.html', context)

    else:
        return redirect('AuthReg:authorisation')

class ItemBySerialNumber(APIView):
    def get(self, request, serial_number):
        try:
            item = Item.objects.get(serial_number=serial_number)
            serializer = ItemSerializer(item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Item.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)


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

def move_item(request):
    if request.method == 'POST':
        form = ItemMovementForm(request.POST, user=request.user)
        if form.is_valid():
            movement = form.save(commit=False)
            movement.from_warehouse = movement.item.warehouse 
            movement.user = request.user
            movement.save()

            movement.item.warehouse = movement.to_warehouse
            movement.item.description = form.cleaned_data['new_description'] or movement.item.description
            movement.item.save()

            return redirect('item_movement_log')
    else:
        form = ItemMovementForm(user=request.user)

    return render(request, 'move_item.html', {'form': form})

def item_movement_log(request):
    movements = ItemMovement.objects.filter(item__warehouse__company=request.user.company).order_by('-timestamp')
    return render(request, 'movement_log.html', {'movements': movements})
from django.shortcuts import render, redirect, get_object_or_404

from AuthReg.models import User
from .forms import ItemMovementForm
from .forms import WarehouseForm, ItemForm

from rest_framework import status

from .models import Warehouse
from .serializers import WarehouseSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q, query
from .serializers import EmployeeSerializer  # Подставь свои сериализаторы



class SearchAPIView(APIView):

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q', None)
from .models import Item, ItemHistory
from .serializers import ItemSerializer, ItemUpdateSerializer
from django.http import JsonResponse

def edit_item(request, warehouse_id, item_id):
    item = get_object_or_404(Item, id=item_id)
    warehouses = Warehouse.objects.filter(company=request.user.company)
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

def create_item(request, warehouse_id):
    parent_warehouse = get_object_or_404(Warehouse, id=warehouse_id)

    if request.method == 'POST':
        form = ItemForm(request.POST, parent_warehouse=parent_warehouse)
        if form.is_valid():
            item = form.save(commit=False)
            item.company = request.user.company  # Привязка к компании
            item.save()
            return redirect('StoreHouse:inventory_by_warehouse', warehouse_id=warehouse_id)
    else:
        form = ItemForm(parent_warehouse=parent_warehouse)

    return render(request, 'StoreHouse/create_item.html', {'form': form, 'parent_warehouse': parent_warehouse})

def delete_item(request, item_id):
    if request.method == 'DELETE':
        item = get_object_or_404(Item, id=item_id)
        item.delete()
        return JsonResponse({'message': 'Item deleted successfully'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def create_warehouse(request, warehouse_id):
    parent_warehouse = get_object_or_404(Warehouse, id=warehouse_id)

    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            warehouse = form.save(commit=False)
            warehouse.company = request.user.company
            warehouse.save()
            return redirect('StoreHouse:inventory_by_warehouse', warehouse_id = warehouse_id)
    else:
        form = WarehouseForm(parent_warehouse=parent_warehouse)
    return render(request, 'StoreHouse/create_warehouse.html', {'form' : form})

def edit_warehouse(request, warehouse_id, warehouse_to_edit):
    warehouse = get_object_or_404(Warehouse, id=warehouse_to_edit)
    warehouses = Warehouse.objects.filter(company=request.user.company)

    if request.method == 'POST':
        form = WarehouseForm(request.POST, instance=warehouse)
        if form.is_valid():
            warehouse = form.save(commit=False)
            warehouse.save()
            return redirect('StoreHouse:inventory_by_warehouse', warehouse_id=warehouse_id)
    else:
        form = WarehouseForm(instance = warehouse)

    return render(request, 'StoreHouse/edit_warehouse.html', {'form': form, 'warehouse': warehouse, 'warehouses': warehouses })


def delete_warehouse(request, warehouse_id):
    if request.method == 'DELETE':
        warehouse = get_object_or_404(Warehouse, id=warehouse_id)
        warehouse.delete()
        return JsonResponse({'message': 'Item deleted successfully'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def inventory(request, warehouse_id=None):
    if request.user.is_authenticated:
        user = request.user
        company = user.company

        if company:
            warehouses = company.warehouses.all()
            if warehouse_id:
                selected_warehouse = get_object_or_404(Warehouse, id=warehouse_id, company=company)
            else:
                selected_warehouse = warehouses.first()

            if selected_warehouse:
                sub_warehouses = selected_warehouse.sub_warehouses.all()
                context = {
                    'company': company,
                    'sub_warehouses': sub_warehouses,
                    'warehouses': warehouses,
                    'selected_warehouse': selected_warehouse,
                }
            else:
                context = {
                'company': None,
                'sub_warehouses': [],
                'warehouses': [],
                'selected_warehouse': [],
                }
        else:
            context = {
                'company': None,
                'sub_warehouses': [],
                'warehouses': [],
                'selected_warehouse': [],
            }

        context.update({        #.update() для словарей - это +=
            'name': user.name,
            'surname': user.surname
        })


        return render(request, 'StoreHouse/inventar.html', context)

    else:
        return redirect('AuthReg:authorisation')

class ItemBySerialNumber(APIView):
    def get(self, request, serial_number):
        try:
            item = Item.objects.get(serial_number=serial_number)
            serializer = ItemSerializer(item, context={'request': request})  # Передаем контекст с запросом
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

def move_item(request):
    if request.method == 'POST':
        form = ItemMovementForm(request.POST, user=request.user)
        if form.is_valid():
            movement = form.save(commit=False)
            movement.from_warehouse = movement.item.warehouse 
            movement.user = request.user
            movement.save()

def action_log(request):
    if request.user.is_authenticated:
        # Получаем все записи истории, связанные с компанией пользователя
        history_records = ItemHistory.objects.filter(company=request.user.company).order_by('-changed_at')

        # Передаем данные в шаблон
        return render(request, 'StoreHouse/action_log.html', {'history_records': history_records, 'name': request.user.name, 'surname': request.user.surname})
    else:
        return redirect('AuthReg:authorisation')
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from StoreHouse.models import Item, Warehouse
from .serializers import InventoryRequestSerializer, ItemSerializer
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import InventoryRequest


def process_inventory_request(request_id):
    try:
        # Загружаем заявку с предзагрузкой связанных предметов
        request = InventoryRequest.objects.prefetch_related('items').get(id=request_id)

        # Проверяем наличие товаров на складе
        missing_items = [item for item in request.items.all() if not item.in_stock]

        if missing_items:
            # Создаем новую заявку на перемещение отсутствующих товаров
            new_request = InventoryRequest.objects.create(
                employee=request.employee,
                status='pending'
            )
            new_request.items.set(missing_items)
            new_request.save()

            return f"Создана новая заявка на перемещение: {new_request.id}"

        # Если все товары на месте, завершаем заявку
        request.status = 'completed'
        request.save()

        return "Заявка успешно завершена"

    except InventoryRequest.DoesNotExist:
        return f"Заявка с ID {request_id} не найдена"


class CompleteInventoryView(APIView):
    def post(self, request, request_id):
        try:
            inventory_request = InventoryRequest.objects.get(id=request_id)

            scanned_items = request.data.get('scanned_items', [])
            missing_items = []
            extra_items = []

            # Проверка отсутствующих товаров
            for item in inventory_request.items.all():
                if item.serial_number not in scanned_items:
                    missing_items.append(item)

            # Проверка лишних товаров
            for serial_number in scanned_items:
                item = Item.objects.filter(serial_number=serial_number).first()
                if not item or item not in inventory_request.items.all():
                    extra_items.append(serial_number)

            # Сохранение данных об отсутствующих и лишних товарах
            inventory_request.missing_items.set(missing_items)
            inventory_request.extra_items.set(Item.objects.filter(serial_number__in=extra_items))
            inventory_request.status = 'completed'
            inventory_request.save()

            return Response({
                "message": "Инвентаризация завершена",
                "missing_items": [item.serial_number for item in missing_items],
                "extra_items": extra_items,
            }, status=status.HTTP_200_OK)

        except InventoryRequest.DoesNotExist:
            return Response({"error": "Заявка не найдена"}, status=status.HTTP_404_NOT_FOUND)



class InventoryRequestPDFView(APIView):
    def get(request, inventory_request_id):
        # Получение данных инвентаризации
        inventory_request = InventoryRequest.objects.get(id=inventory_request_id)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="InventoryRequest_{inventory_request_id}.pdf"'

        pdf = canvas.Canvas(response, pagesize=letter)
        pdf.setTitle(f'Отчет об инвентаризации #{inventory_request_id}')

        # Заголовок
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(100, 750, "Отчет об инвентаризации")

        # Информация о заявке и складе
        pdf.setFont("Helvetica", 12)
        pdf.drawString(100, 730, f"Заявка №: {inventory_request.id}")
        pdf.drawString(100, 710, f"Сотрудник: {inventory_request.employee}")
        pdf.drawString(100, 690, f"Статус: {inventory_request.get_status_display()}")
        pdf.drawString(100, 670, f"Дата дедлайна: {inventory_request.deadline.strftime('%d.%m.%Y %H:%M')}")

        # Список товаров
        pdf.drawString(100, 650, "Товары:")
        y = 630
        for item in inventory_request.items.all():
            pdf.drawString(120, y, f"- {item.name} (Серийный номер: {item.serial_number})")
            y -= 20

        # Сводка
        pdf.drawString(100, y, "Сводка:")
        y -= 20
        pdf.drawString(120, y, f"Количество товаров: {inventory_request.items.count()}")

        pdf.showPage()
        pdf.save()

        return response


class InventoryRequestView(APIView):
    def post(self, request):
        serializer = InventoryRequestSerializer(data=request.data)

        if serializer.is_valid():
            warehouses = serializer.validated_data.get('warehouses', [])
            items = serializer.validated_data.get('items', [])

            # Если предметы не указаны, выбираем все предметы из указанных складов
            if not items and warehouses:
                items = Item.objects.filter(warehouse__in=warehouses)
                serializer.validated_data['items'] = items

            # Создание заявки
            inventory_request = InventoryRequest.objects.create(
                employee=serializer.validated_data['employee'],
                deadline=serializer.validated_data['deadline'],
                status=serializer.validated_data.get('status', 'pending')
            )

            # Присваиваем склады и предметы через метод set()
            inventory_request.warehouses.set(warehouses)
            inventory_request.items.set(items)

            return Response({"message": "Заявка успешно создана", "request_id": inventory_request.id},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        requests = InventoryRequest.objects.all()
        serializer = InventoryRequestSerializer(requests, many=True)
        return Response(serializer.data)

    # PATCH запрос для обновления статуса заявки
    def patch(self, request, request_id):
        try:
            inventory_request = InventoryRequest.objects.get(id=request_id)
            serializer = InventoryRequestSerializer(inventory_request, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except InventoryRequest.DoesNotExist:
            return Response({"error": "Заявка не найдена"}, status=status.HTTP_404_NOT_FOUND)


class InventoryRequestItemsView(APIView):
    def get(self, request, request_id):
        try:
            # Получаем заявку на инвентаризацию по её ID
            inventory_request = InventoryRequest.objects.get(id=request_id)

            # Получаем все предметы, указанные в заявке
            items = inventory_request.items.all()

            # Сериализуем список предметов
            serializer = ItemSerializer(items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except InventoryRequest.DoesNotExist:
            return Response({"error": "Заявка на инвентаризацию не найдена"}, status=status.HTTP_404_NOT_FOUND)
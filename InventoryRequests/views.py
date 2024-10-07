from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import InventoryRequest
from .serializers import InventoryRequestSerializer

class InventoryRequestListCreateView(APIView):
    def get(self, request):
        requests = InventoryRequest.objects.all()
        serializer = InventoryRequestSerializer(requests, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = InventoryRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

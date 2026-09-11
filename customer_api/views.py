import uuid
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Customer, Refund
from .serializers import (
    CustomerSerializer, 
    CustomerHistorySerializer, 
    RefundSerializer,
    PasswordResetResponseSerializer
)

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    # GET /api/customers/{id}/history/
    @action(detail=True, methods=['get'], serializer_class=CustomerHistorySerializer)
    def history(self, request, pk=None):
        customer = self.get_object()
        serializer = self.get_serializer(customer)
        return Response(serializer.data)

    # POST /api/customers/{id}/reset-password/
    @action(detail=True, methods=['post'], serializer_class=PasswordResetResponseSerializer)
    def reset_password(self, request, pk=None):
        customer = self.get_object()
        token = uuid.uuid4().hex
        dummy_link = f"https://miapp.com/reset-password?token={token}&user={customer.id}"
        
        return Response({"reset_link": dummy_link}, status=status.HTTP_200_OK)

class RefundViewSet(viewsets.ModelViewSet):
    queryset = Refund.objects.all()
    serializer_class = RefundSerializer
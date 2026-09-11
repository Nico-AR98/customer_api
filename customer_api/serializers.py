import uuid
from rest_framework import serializers
from django.db import transaction
from .models import Customer, Invoice, Payment, Refund

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'dni', 'email', 'address', 'balance']
        read_only_fields = ['balance']

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'amount', 'issued_at', 'is_paid']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'amount', 'paid_at']

class CustomerHistorySerializer(serializers.ModelSerializer):
    invoices = InvoiceSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'balance', 'invoices', 'payments']

class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = ['id', 'customer', 'amount', 'reason', 'created_at']

    def create(self, validated_data):
        with transaction.atomic():
            customer = validated_data['customer']
            amount = validated_data['amount']
            
            # Se incrementa el saldo del cliente a favor por el reintegro
            customer.balance += amount
            customer.save()
            
            refund = Refund.objects.create(**validated_data)
            return refund

class PasswordResetResponseSerializer(serializers.Serializer):
    reset_link = serializers.CharField()
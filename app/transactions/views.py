from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from transactions import serializers
from django.shortcuts import get_object_or_404
from utils.renderers import CustomRenderer
from products.models import Product
from transactions.models import Transaction
from transactions.exceptions import (
    TransactionValidatedAlready,)
import uuid
from django.contrib.auth import get_user_model
User = get_user_model()


class CreateTransactionAPIView(generics.CreateAPIView):
    """Manage data in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Transaction.objects.all().order_by('-id')
    serializer_class = serializers.TransactionSerializer
    renderer_classes = [CustomRenderer]

    def perform_create(self, serializer):
        """Create new Transaction"""
        product = Product.objects.filter(
            user_id=self.request.user.id).order_by('-id').first()
        amount = self.request.POST.get('amount')
        purchased_hour = float(int(amount)/50000)
        serializer.save(user_id=self.request.user,
                        reference=uuid.uuid4(),
                        purchased_hour=purchased_hour,
                        product_id=product)


class ValidatePaymentAPIView(generics.UpdateAPIView):
    """Manage data in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Transaction.objects.all().order_by('-id')
    serializer_class = serializers.ValidatePaymentSerializer
    renderer_classes = [CustomRenderer]
    lookup_field = 'reference'

    def perform_update(self, serializer):
        """Update transaction status"""
        lookup_field = self.kwargs["reference"]
        transaction = Transaction.objects.filter(
            reference=lookup_field).first()
        if transaction and not transaction.is_active:
            serializer.save(status='success', is_active=True)

            # update the purchased unit for a user
            product = Product.objects.filter(
                user_id=transaction.user_id).first()
            product.unit_in_hours += transaction.purchased_hour
            product.save()
        else:
            raise TransactionValidatedAlready()


class TransactionRetrieveDetail(generics.RetrieveAPIView):
    """Manage data in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Transaction.objects.all().order_by('-id')
    serializer_class = serializers.RetrieveTransactionSerializer
    renderer_classes = [CustomRenderer]
    lookup_field = 'reference'

    def get_object(self):
        lookup_field = self.kwargs["reference"]
        return get_object_or_404(Transaction, reference=lookup_field)


class ListCustomerTransactionAPIView(generics.ListAPIView):
    """Manage data in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Transaction.objects.all().order_by('-id')
    serializer_class = serializers.RetrieveTransactionSerializer
    renderer_classes = [CustomRenderer]

    def get_queryset(self):
        return Transaction.objects.filter(
            user_id=self.request.user.id).order_by('-id')


class ListTransactionAPIView(generics.ListAPIView):
    """Manage data in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Transaction.objects.all().order_by('-id')
    serializer_class = serializers.RetrieveTransactionSerializer
    renderer_classes = [CustomRenderer]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'user_id']

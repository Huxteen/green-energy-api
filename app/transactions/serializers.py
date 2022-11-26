from rest_framework import serializers
from transactions.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Transaction objects"""

    class Meta:
        model = Transaction
        ordering = ['-id']
        read_only_fields = ('id', 'status', 'reference', 'purchased_hour')
        fields = ('id',
                  'amount',
                  'reference',
                  'payment_channel',
                  'purchased_hour',
                  'status')


class ValidatePaymentSerializer(serializers.ModelSerializer):
    """Serializer for Validate Payment objects"""

    class Meta:
        model = Transaction
        ordering = ['-id']
        read_only_fields = ('id',
                            'amount',
                            'status',
                            'reference',
                            'payment_channel',
                            'is_active',
                            'purchased_hour')
        fields = ('id',
                  'amount',
                  'reference',
                  'payment_channel',
                  'is_active',
                  'purchased_hour',
                  'status')


class RetrieveTransactionSerializer(serializers.ModelSerializer):
    """Serializer to Retrieve Transaction objects"""

    class Meta:
        model = Transaction
        ordering = ['-id']
        fields = '__all__'

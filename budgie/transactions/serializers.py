from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'category', 'transaction_type', 'amount', 'date', 'description']
        extra_kwargs = {'user': {'read_only': True}}
        read_only_fields = ['id', 'user']
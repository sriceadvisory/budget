from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from .serializers import TransactionSerializer
from .filters import TransactionFilter
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView

# Create your views here.
class TransactionListCreateView(ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filterset_class = TransactionFilter
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    ordering_fields = ['date']
    ordering = ['-date']
    search_fields = ['description']

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class TransactionRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionFilter
    pagination_class = PageNumberPagination
    ordering_fields = ['date']
    ordering = ['-date']
    search_fields = ['description']

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class TransactionDetailView(RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
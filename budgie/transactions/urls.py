from django.urls import path
from .views import TransactionListCreateView, TransactionRetrieveUpdateDeleteView

urlpatterns = [
    path('transactions/', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('transactions/<uuid:pk>/', TransactionRetrieveUpdateDeleteView.as_view(), name='transaction-retrieve-update-delete'),
]
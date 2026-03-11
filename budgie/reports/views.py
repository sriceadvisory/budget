from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Sum

from transactions.models import Transaction
from .serializers import MonthlyReportSerializer, AnnualReportSerializer


class MonthlyReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        if not month or not year:
            return Response(
                {'error': 'month and year query parameters are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            month = int(month)
            year = int(year)
        except ValueError:
            return Response(
                {'error': 'month and year must be valid integers.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        transactions = Transaction.objects.filter(
            user=request.user,
            date__month=month,
            date__year=year
        )

        data = _build_report(transactions)
        data.update({'month': month, 'year': year})

        serializer = MonthlyReportSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AnnualReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        year = request.query_params.get('year')

        if not year:
            return Response(
                {'error': 'year query parameter is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            year = int(year)
        except ValueError:
            return Response(
                {'error': 'year must be a valid integer.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        transactions = Transaction.objects.filter(
            user=request.user,
            date__year=year
        )

        data = _build_report(transactions)
        data.update({'year': year})

        serializer = AnnualReportSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


def _build_report(transactions):
    """Shared aggregation logic for both monthly and annual reports."""
    income_qs = transactions.filter(transaction_type='income')
    expense_qs = transactions.filter(transaction_type='expense')

    total_income = income_qs.aggregate(total=Sum('amount'))['total'] or 0
    total_expense = expense_qs.aggregate(total=Sum('amount'))['total'] or 0

    income_by_category = [
        {'category': item['category__name'], 'amount': item['total']}
        for item in income_qs.values('category__name').annotate(total=Sum('amount'))
    ]
    expense_by_category = [
        {'category': item['category__name'], 'amount': item['total']}
        for item in expense_qs.values('category__name').annotate(total=Sum('amount'))
    ]

    return {
        'total_income': total_income,
        'total_expense': total_expense,
        'net_balance': total_income - total_expense,
        'income_by_category': income_by_category,
        'expense_by_category': expense_by_category,
    }
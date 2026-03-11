from rest_framework import serializers


# --- Reusable base ---

class CategoryAmountSerializer(serializers.Serializer):
    category = serializers.CharField(max_length=255)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)


class ReportSummarySerializer(serializers.Serializer):
    total_income = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_expense = serializers.DecimalField(max_digits=10, decimal_places=2)
    net_balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    income_by_category = CategoryAmountSerializer(many=True)
    expense_by_category = CategoryAmountSerializer(many=True)


# --- Report-level serializers ---

class MonthlyReportSerializer(ReportSummarySerializer):
    month = serializers.IntegerField(min_value=1, max_value=12)
    year = serializers.IntegerField()


class AnnualReportSerializer(ReportSummarySerializer):
    year = serializers.IntegerField()
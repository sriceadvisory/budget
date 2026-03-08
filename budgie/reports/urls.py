from django.urls import path
from .views import MonthlyReportView, AnnualReportView

urlpatterns = [
    path('reports/monthly/', MonthlyReportView.as_view(), name='monthly-report'),
    path('reports/annual/', AnnualReportView.as_view(), name='annual-report'),
]
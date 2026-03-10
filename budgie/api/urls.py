from rest_framework.routers import DefaultRouter
from transactions.views import TransactionViewSet
from categories.views import CategoryViewSet
from reports.views import ReportViewSet

router = DefaultRouter()  # DefaultRouter gives you the root view for free
router.register('transactions', TransactionViewSet, basename='transaction')
router.register('categories', CategoryViewSet, basename='category')
router.register('reports', ReportViewSet, basename='report')

urlpatterns = router.urls
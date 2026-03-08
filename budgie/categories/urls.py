from django.urls import path
from .views import CategoryListCreateView, CategoryRetrieveUpdateDeleteView

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<uuid:pk>/', CategoryRetrieveUpdateDeleteView.as_view(), name='category-retrieve-update-delete'),
]
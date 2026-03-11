from django_filters import FilterSet

from .models import Category


class CategoryFilter(FilterSet):
    class Meta:
        model = Category
        fields = ["type", "name"]


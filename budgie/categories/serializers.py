from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'type']
        extra_kwargs = {'user': {'read_only': True}}
        read_only_fields = ['id', 'user']
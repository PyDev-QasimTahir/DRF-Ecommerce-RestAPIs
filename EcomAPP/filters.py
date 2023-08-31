from django_filters.rest_framework import FilterSet
from .models import Product, Company, Category


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['exact'],
            'company': ['exact'],
            'category': ['exact']
        }


class CompanytFilter(FilterSet):
    class Meta:
        model = Company
        fields = {
            'name': ['exact'],
        }

class CategorytFilter(FilterSet):
    class Meta:
        model = Category
        fields = {
            'name': ['exact'],
        }
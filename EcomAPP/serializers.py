from django.conf import settings
from rest_framework import serializers
from .models import Product, Category, Company, AddCart, ShipInfo, PaymentMethod
from django.contrib.auth.models import User


# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


# Company Serializer
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


# Signup Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user


# Add to Cart Serializer
class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddCart
        fields = ('user', 'product', 'quantity', 'added_at', 'total_price')


# Shipping Info:-
class ShipInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipInfo
        fields = '__all__'


# Payment Method:-
class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ('product_cart', 'cardholder_name', 'card_number', 'exp_month', 'exp_year', 'cvv')

    def validate_card_number(self, value):
        if len(value) != 16:
            raise serializers.ValidationError("Length of card number must be 16")
        return value

    def validate_exp_month(self, value):
        if not value.isdigit() or not (1 <= int(value) <= 12):
            raise serializers.ValidationError("Invalid month")
        return value

    def validate_exp_year(self, value):
        if not int(value) >= 23:
            raise serializers.ValidationError("Invalid year")
        return value

    def validate_cvv(self, value):
        if len(value) != 3:
            raise serializers.ValidationError("Length of CSC must be 3")
        return value

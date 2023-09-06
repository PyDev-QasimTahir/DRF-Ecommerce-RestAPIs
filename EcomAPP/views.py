import stripe
from .models import *
from .serializers import *
from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.authtoken.models import Token
from djstripe.models import PaymentMethod, Customer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from .filters import ProductFilter, CompanytFilter, CategorytFilter
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

# Category Code
class CategoryShowAdd(APIView):
    def get(self, request, format=None):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)
        filter_backends = [DjangoFilterBackend, SearchFilter]
        filterset_class = CategoryFilter
        search_fields = ['name']
        throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDeleteUpdateRetrieve(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        throttle_classes = [AnonRateThrottle, UserRateThrottle]
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Product Code,
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']
    pagination_class = LimitOffsetPagination



class ProductRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated,)


# Company Code
class CompanyListCreateAPIView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CompanytFilter
    search_fields = ['name']
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

class CompanyRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


# Sign-up API
class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


# Logout API
class UserLogoutView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"detail": "Logged out successfully."})


# Add-to-Cart view
class AddToCartView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        product_id = request.data.get('product')
        quantity = request.data.get('quantity', 1)

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        cart_item, created = AddCart.objects.get_or_create(user=request.user, product=product)
        cart_item.quantity += int(quantity)
        cart_item.total = cart_item.quantity * product.price
        cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Shipping Information view:
class ShipInfoListCreateAPIView(generics.ListCreateAPIView):
    queryset = ShipInfo.objects.all()
    serializer_class = ShipInfoSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ShipInfoRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShipInfo.objects.all()
    serializer_class = ShipInfoSerializer
    permission_classes = (permissions.IsAuthenticated,)


# Payment Method
class CreatePaymentMethodView(generics.CreateAPIView):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, request, serializer):
        user = self.request.user
        serializer.save(user=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            payment_method = serializer.save(user = self.request.user)

            success_message = "Congrats, Your Payment was Successfully Done."

            response_data = {
                "message": success_message,
                "payment_method": serializer.data
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


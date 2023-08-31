from django.db import models
from django.contrib.auth.models import User


# Company Mode
class Company(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# Category Model
class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# Product Model
class Product(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    storage = models.CharField(max_length=200)
    description = models.TextField()
    discount_offer = models.CharField(max_length=200)
    discount_price = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return self.name



class AddCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s cart - {self.product.name}"


class ShipInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product_cart = models.ForeignKey(AddCart, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    area_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=5)

    def __str__(self):
        return str(self.user)


# class PaymentMethod(DjstripePaymentMethod):
class PaymentMethod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product_cart = models.ForeignKey(AddCart, on_delete=models.CASCADE, null=True, blank=True)
    cardholder_name = models.CharField(max_length=50)
    card_number = models.CharField(max_length=16)
    exp_month = models.CharField(max_length=2)
    exp_year = models.CharField(max_length=2)
    cvv = models.CharField(max_length=3)

    def __str__(self):
        return str(self.cardholder_name)

    def attach_to_customer(self, customer):
        self.customer = customer
        self.save()

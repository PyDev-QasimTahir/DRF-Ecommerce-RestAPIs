from django.contrib import admin
from .models import Product, Company, Category, ShipInfo, AddCart, PaymentMethod

# Register your models here.
admin.site.register(Product)
admin.site.register(Company)
admin.site.register(Category)
admin.site.register(ShipInfo)
admin.site.register(AddCart)
admin.site.register(PaymentMethod)

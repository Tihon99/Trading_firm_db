from django.contrib import admin
from .models import *
admin.site.register(Budget)
admin.site.register(Categories)
admin.site.register(Product)
admin.site.register(Suppliers)
admin.site.register(SupplierProduct)
admin.site.register(SupplierOrders)
admin.site.register(Customers)
admin.site.register(Orders)
admin.site.register(Returns)
admin.site.register(Warehouse)
admin.site.register(PriceChanges)
admin.site.register(SuppliersPriceChanges)

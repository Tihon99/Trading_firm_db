from django.db import models

class Budget(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=4)
    date = models.DateTimeField(auto_now_add=True)

class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()

class Suppliers(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    contactInfo = models.TextField()

class SupplierProduct(models.Model):
    id = models.AutoField(primary_key=True)
    supplierID = models.ForeignKey(Suppliers, on_delete=models.CASCADE)
    productID = models.ForeignKey(Product, on_delete=models.CASCADE)
    salePercents = models.DecimalField(max_digits=10, decimal_places=4)
    quantitySale = models.DecimalField(max_digits=10, decimal_places=4)

class SupplierOrders(models.Model):
    id = models.AutoField(primary_key=True)
    supplierProductID = models.ForeignKey(SupplierProduct, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=4)
    orderDate = models.DateTimeField(auto_now_add=True)

class SuppliersPriceChanges(models.Model):
    supplierProductID = models.ForeignKey(SupplierProduct, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    newPrice = models.DecimalField(max_digits=10, decimal_places=2)

class PriceChanges(models.Model):
    productID = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    newPrice = models.DecimalField(max_digits=10, decimal_places=4)

class Customers(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    contactInfo = models.TextField()

class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    customerID = models.ForeignKey(Customers, on_delete=models.CASCADE)
    productID = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=4)
    orderDate = models.DateTimeField(auto_now_add=True)

class Returns(models.Model):
    id = models.AutoField(primary_key=True)
    orderID = models.ForeignKey(Orders, on_delete=models.CASCADE)
    orderDate = models.DateTimeField(auto_now_add=True)

class Warehouse(models.Model):
    productID = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=4)
    date = models.DateTimeField(auto_now_add=True)

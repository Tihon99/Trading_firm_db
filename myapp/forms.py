from django import forms
from .models import *
class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['customerID', 'productID', 'quantity']

class SupplierOrderForm(forms.ModelForm):
    class Meta:
        model = SupplierOrders
        fields = ['supplierProductID', 'quantity']

class ReturnForm(forms.ModelForm):
    class Meta:
        model = Returns
        fields = ['orderID']

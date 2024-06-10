from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_order/', views.create_order, name='create_order'),
    path('create_supplier_order/', views.create_supplier_order, name='create_supplier_order'),
    path('create_return/', views.create_return, name='create_return'),
    path('warehouse_report/', views.warehouse_report, name='warehouse_report'),
    path('orders_report/', views.orders_report, name='orders_report'),
    path('financial_report/', views.financial_report, name='financial_report'),
    path('financial_analysis/', views.financial_analysis, name='financial_analysis'),
]

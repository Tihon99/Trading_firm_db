from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime, timedelta
from .models import *
from .forms import *
from django.db.models import F, Subquery, OuterRef, DecimalField, ExpressionWrapper, Sum
from django.db.models.functions import Coalesce
from django.utils import timezone
from datetime import timedelta

def index(request):
    return render(request, 'index.html')

def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            product = order.productID
            quantity_needed = order.quantity
            warehouse_item = Warehouse.objects.get(productID=product)
            price_change = PriceChanges.objects.filter(productID=product).latest('date')

            # проверка хватает ли товара на складе
            if warehouse_item.quantity < quantity_needed:
                # вычесление сколько нужно заказать товара у поставщика
                quantity_to_order = quantity_needed - warehouse_item.quantity

                # вычесление суммы, на которую будет произведене заказа у поставщика
                supplier_product = SupplierProduct.objects.get(productID=product)
                supplier_price_change = SuppliersPriceChanges.objects.filter(supplierProductID=supplier_product.id).latest('date')

                # проверка на предоставление скидки
                if (quantity_to_order >= supplier_product.quantitySale):
                    supplier_order_cost = supplier_price_change.newPrice * supplier_product.salePercents // 100 * quantity_to_order
                else:
                    supplier_order_cost = supplier_price_change.newPrice * quantity_to_order

                # проверка на то, что бюджета хватит, чтобы заказать товар
                current_budget = Budget.objects.latest('date')
                if current_budget.amount >= supplier_order_cost:
                    # создание заказа поставщику
                    SupplierOrders.objects.create(
                        supplierProductID=supplier_product,
                        quantity=quantity_to_order
                    )
                    # вычитание средств из нашего бюджета
                    current_budget.amount -= supplier_order_cost
                else:
                    return HttpResponse("Not enough budget to create supplier order.")

            # проверка, что товар на складе не уйдет в минус
            if (warehouse_item.quantity - quantity_needed < 0):
                warehouse_item.quantity = 0
            else:
                warehouse_item.quantity -= quantity_needed
            warehouse_item.save()

            # добавление в бюджет суммы, на которую был оформлен заказ потребителем
            current_budget = Budget.objects.latest('date')
            current_budget.amount += quantity_needed * price_change.newPrice
            current_budget.save()

            return render(request, 'create_order.html', {'form': form})
    else:
        form = OrderForm()
    return render(request, 'create_order.html', {'form': form})


def create_supplier_order(request):
    if request.method == 'POST':
        form = SupplierOrderForm(request.POST)
        if form.is_valid():
            supplier_order = form.save()

            # определение суммы заказа
            supplier_product = supplier_order.supplierProductID
            supplier_price_change = SuppliersPriceChanges.objects.filter(supplierProductID=supplier_product.id).latest('date')

            #проверка на предоставление скидки
            if (supplier_order.quantity >= supplier_product.quantitySale):
                supplier_order_cost = supplier_price_change.newPrice * supplier_product.salePercents // 100 * supplier_order.quantity
            else:
                supplier_order_cost = supplier_price_change.newPrice * supplier_order.quantity
            current_budget = Budget.objects.latest('date')

            # проверка на наличие бюджета для заказа
            if current_budget.amount >= supplier_order_cost:
                current_budget.amount -= supplier_order_cost
                current_budget.save()

                # перенос купленного количества товара на склад
                warehouse_item = Warehouse.objects.get(productID=supplier_product.productID)
                warehouse_item.quantity += supplier_order.quantity
                warehouse_item.save()
            else:
                return HttpResponse("Not enough budget to create supplier order.")
            return render(request, 'create_supplier_order.html', {'form': form})
    else:
        form = SupplierOrderForm()
    return render(request, 'create_supplier_order.html', {'form': form})


def create_return(request):
    if request.method == 'POST':
        form = ReturnForm(request.POST)
        if form.is_valid():
            return_instance = form.save(commit=False)
            order = return_instance.orderID
            product = order.productID

            # проверка, что товар не принадлежит категории 'материалы'
            if product.category.name != 'materials':
                # полный возврат средств потребителю
                price_change = PriceChanges.objects.filter(productID=product).latest('date')
                refund_amount = price_change.newPrice * order.quantity
                current_budget = Budget.objects.latest('date')
                current_budget.amount -= refund_amount
                current_budget.save()

                # возвращение этого товара на склад
                warehouse_item = Warehouse.objects.get(productID=product)
                warehouse_item.quantity += order.quantity
                warehouse_item.save()

                # сохранение возврата и удаление заказа из списка заказов
                return_instance.save()
                order.delete()
            else:
                return_instance.save()

            return render(request, 'create_return.html', {'form': form})
    else:
        form = ReturnForm()
    return render(request, 'create_return.html', {'form': form})


def warehouse_report(request):
    warehouse_items = Warehouse.objects.all()
    return render(request, 'warehouse_report.html', {'warehouse_items': warehouse_items})


def orders_report(request):
    if request.method == 'POST':
        # определение периода оценки заказов
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        orders = Orders.objects.filter(orderDate__range=[start_date, end_date])

        return render(request, 'orders_report.html', {'orders': orders})
    return render(request, 'orders_report_form.html')


def financial_report(request):
    # текущий бюджет
    current_budget = Budget.objects.latest('date')

    # финансовое состояние склада
    warehouse_value = Warehouse.objects.aggregate(
        total_value=Sum(F('productID__pricechanges__newPrice') * F('quantity'))
    )

    total_value = current_budget.amount + warehouse_value['total_value']

    return render(request, 'financial_report.html', {'total_value': total_value})

def financial_analysis(request):
    current_year = datetime.now().year

    # Subquery для получения последней цены на момент заказа для Products
    latest_price_subquery = PriceChanges.objects.filter(
        productID=OuterRef('productID'),
        date__lte=OuterRef('orderDate')
    ).order_by('-date').values('newPrice')[:1]

    # Subquery для получения последней цены на момент заказа для SupplierProducts
    latest_supplier_price_subquery = SuppliersPriceChanges.objects.filter(
        supplierProductID=OuterRef('supplierProductID'),
        date__lte=OuterRef('orderDate')
    ).order_by('-date').values('newPrice')[:1]

    # QuerySet для Orders с вычисленной стоимостью
    orders = Orders.objects.filter(orderDate__year=current_year).annotate(
        latest_price=Subquery(latest_price_subquery),
        total_price=ExpressionWrapper(F('quantity') * Coalesce(F('latest_price'), 0), output_field=DecimalField(max_digits=10, decimal_places=2))
    ).values('id', 'orderDate', 'total_price')

    # QuerySet для SupplierOrders с вычисленной стоимостью
    supplier_orders = SupplierOrders.objects.filter(orderDate__year=current_year).annotate(
        latest_price=Subquery(latest_supplier_price_subquery),
        total_price=ExpressionWrapper(F('quantity') * Coalesce(F('latest_price'), 0), output_field=DecimalField(max_digits=10, decimal_places=2))
    ).values('id', 'orderDate', 'total_price')

    context = {
        'orders': orders,
        'supplier_orders': supplier_orders,
    }

    return render(request, 'financial_analysis.html', context)

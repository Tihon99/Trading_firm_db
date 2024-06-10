import os
import sys
import time
from django.db import transaction, models
from decimal import Decimal

class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()

# Функция для заполнения таблицы Product тестовыми данными
def populate_products(n):
    category = Categories.objects.create(name='test_category')
    products = [
        Product(category=category, name=f'Product {i}', description=f'Description for product {i}')
        for i in range(n)
    ]
    Product.objects.bulk_create(products)

# Функция для измерения времени выполнения операции
def measure_time(operation, *args, **kwargs):
    start_time = time.time()
    operation(*args, **kwargs)
    end_time = time.time()
    return end_time - start_time

# Операции
def search_by_key():
    Product.objects.get(pk=1)

def search_by_non_key():
    Product.objects.filter(name='Product 1')

def search_by_pattern():
    Product.objects.filter(name__contains='Product')

def add_record():
    category = Categories.objects.get(name='test_category')
    Product.objects.create(category=category, name='New Product', description='Description')

def add_records_group(n):
    category = Categories.objects.get(name='test_category')
    products = [
        Product(category=category, name=f'New Product {i}', description=f'Description {i}')
        for i in range(n)
    ]
    Product.objects.bulk_create(products)

def update_record_by_key():
    product = Product.objects.get(pk=1)
    product.name = 'Updated Product'
    product.save()

def update_record_by_non_key():
    product = Product.objects.filter(name='Product 1').first()
    product.name = 'Updated Product'
    product.save()

def delete_record_by_key():
    Product.objects.get(pk=1).delete()

def delete_record_by_non_key():
    Product.objects.filter(name='Product 1').first().delete()

def delete_records_group(n):
    Product.objects.all()[:n].delete()

def compress_database():
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute('VACUUM;')

# Основная функция для тестирования
def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
    # Установить количество записей для тестирования
    records_counts = [1000, 10000, 100000]
    results = {}

    for count in records_counts:
        print(f'Testing with {count} records')
        # Заполнить таблицу тестовыми данными
        populate_products(count)
        results[count] = {}

        # Измерить время выполнения каждой операции
        results[count]['search_by_key'] = measure_time(search_by_key)
        results[count]['search_by_non_key'] = measure_time(search_by_non_key)
        results[count]['search_by_pattern'] = measure_time(search_by_pattern)
        results[count]['add_record'] = measure_time(add_record)
        results[count]['add_records_group'] = measure_time(add_records_group, count)
        results[count]['update_record_by_key'] = measure_time(update_record_by_key)
        results[count]['update_record_by_non_key'] = measure_time(update_record_by_non_key)
        results[count]['delete_record_by_key'] = measure_time(delete_record_by_key)
        results[count]['delete_record_by_non_key'] = measure_time(delete_record_by_non_key)
        results[count]['delete_records_group'] = measure_time(delete_records_group, count // 10)
        results[count]['compress_database'] = measure_time(compress_database)

        # Очистить таблицу перед следующим тестом
        Product.objects.all().delete()

    # Вывести результаты
    for count, timings in results.items():
        print(f'\nResults for {count} records:')
        for operation, time_taken in timings.items():
            print(f'{operation}: {time_taken:.4f} seconds')

if __name__ == "__main__":
    main()

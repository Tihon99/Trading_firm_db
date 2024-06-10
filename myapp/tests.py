import timeit
from django.test import TestCase
from .models import Categories, Product

class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Categories.objects.create(name='TestCategory')

    def create_products(self, number_of_products):
        Product.objects.all().delete()  # Очистить существующие записи
        products = [
            Product(
                category=self.category,
                name=f'TestProduct{i}',
                description=f'TestDescription{i}'
            )
            for i in range(number_of_products)
        ]
        Product.objects.bulk_create(products)

    def test_operations(self):
        record_counts = [1000, 10000, 100000]
        for count in record_counts:
            self.create_products(count)
            print(f'\nTesting with {count} records')

            mid_id = Product.objects.all()[count // 2].id  # Использование средней записи

            self.measure_time('Search by primary key', lambda: Product.objects.get(id=mid_id))
            self.measure_time('Search by non-primary key', lambda: Product.objects.get(name=f'TestProduct{count // 2}'))
            self.measure_time('Search by mask', lambda: Product.objects.filter(name__contains='Product'))
            self.measure_time('Add record', lambda: Product.objects.create(
                category=self.category,
                name='NewProduct',
                description='NewDescription'
            ))
            self.measure_time('Add multiple records', self.add_multiple_records)
            self.measure_time('Update record by primary key', lambda: Product.objects.filter(id=mid_id).update(description='UpdatedDescription'))
            self.measure_time('Update record by non-primary key', lambda: Product.objects.filter(name=f'TestProduct{count // 2}').update(description='UpdatedDescription'))
            self.measure_time('Delete record by primary key', lambda: Product.objects.get(id=mid_id).delete())
            self.measure_time('Delete record by non-primary key', lambda: Product.objects.filter(name=f'TestProduct{count // 2}').delete())
            self.measure_time('Delete multiple records', lambda: Product.objects.filter(id__lte=200).delete())
            self.measure_time('Compress database after deleting 200 rows', self.compress_db_after_deleting_200)
            self.measure_time('Compress database after retaining 200 rows', self.compress_db_after_retaining_200)

    def measure_time(self, operation_name, func):
        elapsed_time = timeit.timeit(func, number=1)
        print(f'{operation_name}: {elapsed_time:.6f} seconds')

    def add_multiple_records(self):
        products = [
            Product(
                category=self.category,
                name=f'NewProduct{i}',
                description=f'NewDescription{i}'
            )
            for i in range(100)
        ]
        Product.objects.bulk_create(products)

    def compress_db_after_deleting_200(self):
        initial_count = Product.objects.count()
        products_to_delete = Product.objects.all()[:200]
        Product.objects.filter(id__in=products_to_delete).delete()
        remaining_count = Product.objects.count()
        print(f'Initial count: {initial_count}, Remaining count after deleting 200: {remaining_count}')
        # Simulate compression operation (if your DB supports it, you might call an actual DB command here)
        self.simulate_db_compression()

    def compress_db_after_retaining_200(self):
        Product.objects.exclude(id__in=Product.objects.values_list('id', flat=True)[:200]).delete()
        remaining_count = Product.objects.count()
        print(f'Remaining count after retaining 200: {remaining_count}')
        # Simulate compression operation (if your DB supports it, you might call an actual DB command here)
        self.simulate_db_compression()

    def simulate_db_compression(self):
        # Placeholder for database compression logic, if any.
        # Some databases like SQLite do not require explicit compression.
        pass

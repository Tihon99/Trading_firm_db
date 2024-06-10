# Generated by Django 5.0.6 on 2024-05-31 11:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_remove_returns_productid_remove_returns_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuppliersPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('newPrice', models.DecimalField(decimal_places=2, max_digits=10)),
                ('supplierProductID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.supplierproduct')),
            ],
        ),
        migrations.DeleteModel(
            name='SuppliersPriceChanges',
        ),
    ]
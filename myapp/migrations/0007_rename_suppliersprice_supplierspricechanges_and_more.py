# Generated by Django 5.0.6 on 2024-05-31 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_suppliersprice1'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SuppliersPrice',
            new_name='SuppliersPriceChanges',
        ),
        migrations.DeleteModel(
            name='SuppliersPrice1',
        ),
    ]

# Generated by Django 5.0.6 on 2024-05-30 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]

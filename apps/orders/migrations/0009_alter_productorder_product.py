# Generated by Django 5.1.7 on 2025-05-21 18:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_order_is_delivered'),
        ('products', '0006_alter_product_batch_packages_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productorder',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product'),
        ),
    ]

# Generated by Django 5.1.7 on 2025-05-01 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_status_identifier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='identifier',
            field=models.IntegerField(),
        ),
    ]

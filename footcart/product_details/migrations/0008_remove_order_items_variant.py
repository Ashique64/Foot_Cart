# Generated by Django 4.2.4 on 2023-08-31 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product_details', '0007_order_items_variant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order_items',
            name='variant',
        ),
    ]

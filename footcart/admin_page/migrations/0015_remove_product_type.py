# Generated by Django 4.2.4 on 2023-08-08 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_page', '0014_alter_product_discount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='type',
        ),
    ]

# Generated by Django 4.2.4 on 2023-09-17 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_page', '0041_remove_wishlist_products_wishlist_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variants',
            name='discount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='variants',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]

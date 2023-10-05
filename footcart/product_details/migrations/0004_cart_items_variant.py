# Generated by Django 4.2.4 on 2023-08-26 05:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_page', '0028_alter_variants_discount'),
        ('product_details', '0003_alter_order_items_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart_items',
            name='variant',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, to='admin_page.variants'),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.2.4 on 2023-08-17 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_page', '0022_color_size_my_order_address_my_order_payment_method_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='size',
            name='name',
            field=models.PositiveIntegerField(),
        ),
    ]

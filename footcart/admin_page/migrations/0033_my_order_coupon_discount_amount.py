# Generated by Django 4.2.4 on 2023-09-10 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_page', '0032_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='my_order',
            name='coupon_discount_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
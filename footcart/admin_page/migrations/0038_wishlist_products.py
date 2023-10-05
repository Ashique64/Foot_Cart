# Generated by Django 4.2.4 on 2023-09-12 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_page', '0037_remove_wishlist_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlist',
            name='products',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='admin_page.product'),
            preserve_default=False,
        ),
    ]
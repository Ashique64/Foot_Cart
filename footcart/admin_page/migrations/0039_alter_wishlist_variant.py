# Generated by Django 4.2.4 on 2023-09-12 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_page', '0038_wishlist_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='variant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_page.variants'),
        ),
    ]

# Generated by Django 4.2.4 on 2023-08-28 08:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_page', '0028_alter_variants_discount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='my_order',
            name='product',
        ),
    ]

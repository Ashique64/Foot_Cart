# Generated by Django 4.2.4 on 2023-08-07 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile_pages', '0004_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='alter_phone',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='phone_number',
            field=models.IntegerField(),
        ),
    ]

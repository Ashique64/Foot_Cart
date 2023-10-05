# Generated by Django 4.2.4 on 2023-08-07 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profile_pages', '0003_delete_personal_information'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('phone_number', models.IntegerField(max_length=10)),
                ('pincode', models.IntegerField()),
                ('locality', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=150)),
                ('district', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('landmark', models.CharField(blank=True, max_length=50, null=True)),
                ('alter_phone', models.IntegerField(blank=True, max_length=10, null=True)),
            ],
        ),
    ]
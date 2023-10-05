# Generated by Django 4.2.4 on 2023-08-07 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_user_details_is_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_details',
            name='age',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user_details',
            name='gender',
            field=models.CharField(default=2, max_length=10),
            preserve_default=False,
        ),
    ]

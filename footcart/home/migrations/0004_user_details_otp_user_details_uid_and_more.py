# Generated by Django 4.2.3 on 2023-07-22 11:34

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_user_details_groups_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_details',
            name='otp',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='user_details',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='user_details',
            name='phone_number',
            field=models.CharField(max_length=13),
        ),
    ]

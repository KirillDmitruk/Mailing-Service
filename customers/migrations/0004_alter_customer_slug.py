# Generated by Django 4.2.2 on 2024-06-23 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_customer_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='slug',
            field=models.CharField(blank=True, max_length=150, null=True, unique=True, verbose_name='URL'),
        ),
    ]

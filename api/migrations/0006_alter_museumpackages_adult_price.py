# Generated by Django 4.2.6 on 2023-10-19 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_museumpackages_delete_museumpackage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='museumpackages',
            name='adult_price',
            field=models.IntegerField(verbose_name='Enter the price for Adults (19-99) in USD'),
        ),
    ]

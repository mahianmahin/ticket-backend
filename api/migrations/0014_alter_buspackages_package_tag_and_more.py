# Generated by Django 4.2.6 on 2023-10-30 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_purchasedtickets_qr_content_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buspackages',
            name='package_tag',
            field=models.IntegerField(default=62983),
        ),
        migrations.AlterField(
            model_name='museumpackages',
            name='package_tag',
            field=models.IntegerField(default=37178),
        ),
    ]
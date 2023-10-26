# Generated by Django 4.2.6 on 2023-10-26 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_alter_buspackages_package_tag_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchasedTickets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(blank=True, max_length=500, null=True)),
                ('package', models.CharField(blank=True, max_length=1000, null=True)),
                ('total_price', models.IntegerField(default=0)),
                ('adults', models.IntegerField(default=0)),
                ('youths', models.IntegerField(default=0)),
                ('infants', models.IntegerField(default=0)),
                ('selected_date', models.CharField(blank=True, max_length=20, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('package_tag', models.IntegerField(default=0)),
                ('package_unique_identifier', models.IntegerField(default=0)),
                ('qr_code', models.ImageField(upload_to='qr_codes')),
                ('qr_code_scanned', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='buspackages',
            name='package_tag',
            field=models.IntegerField(default=59535),
        ),
        migrations.AlterField(
            model_name='museumpackages',
            name='package_tag',
            field=models.IntegerField(default=46804),
        ),
    ]

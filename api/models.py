import random
from io import BytesIO

import qrcode
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.core.files import File
from django.db import models
from PIL import Image, ImageDraw


def random_number():
    return random.randint(10000,99999)

class HeroImage(models.Model):
    image = models.ImageField(upload_to="hero_images")

class TicketFolders(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to="folder_images")

    def __str__(self):
        return self.name
    

class BusPackages(models.Model):
    class Type(models.TextChoices):
        TYPE_24_HOURS = '24 hours', '24 Hours',
        TYPE_48_HOURS = '48 hours', '48 Hours',
        TYPE_72_HOURS = '72 hours', '72 Hours',
        TYPE_1_DAY = '1 day', '1 Day',
        TYPE_3_PASS = '3 pass', '3 Pass',
        TYPE_DAILY_TOUR = 'daily tour', 'Daily tour',
        TYPE_HALF_DAY = 'half day', 'Half day',
        TYPE_ONE_RUN = 'one run', 'One run'

    class Company(models.TextChoices):
        BIG_BUS = 'big bus', 'Big bus',
        GREEN_LINE = 'green line', 'Green line',
        I_LOVE_ROME = 'i love rome', 'I love rome',
        IO_BUS = 'io_bus', 'IO bus',
        CITY_SIGHTSEEING = 'city sightseeing', 'City sightseeing'


    folder = models.ForeignKey(TicketFolders, on_delete=models.CASCADE, null=True)
    purchased_date = models.DateTimeField(auto_now=True)
    image_big = models.ImageField(upload_to="bus_packages")
    type = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    duration = models.CharField(max_length=20, null=True, blank=True)

    second_image = models.ImageField(upload_to="bus_packages")
    third_image = models.ImageField(upload_to="bus_packages")
    fourth_image = models.ImageField(upload_to="bus_packages")

    description = RichTextField()

    off_price = models.IntegerField(verbose_name="Enter the off price (USD)")
    adult_price = models.IntegerField(verbose_name="Enter the price for Adults (19-99) in USD")
    youth_price = models.IntegerField(verbose_name="Enter the price for Youths (6-18) in USD")
    infant_price = models.IntegerField(verbose_name="Enter the price for Infants (0-5) in USD")

    package_tag = models.IntegerField(editable=False)
    is_featured = models.BooleanField(default=False)

    ticket_type = models.CharField(max_length=100, choices=Type.choices, null=True, blank=True)
    company = models.CharField(max_length=100, choices=Company.choices, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.package_tag:
            self.package_tag = random_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title or "Untitled Package"


class Date(models.Model):
    date = models.DateField()

    def __str__(self):
        return str(self.date)


class MuseumPackages(models.Model):
    folder = models.ForeignKey(TicketFolders, on_delete=models.CASCADE, null=True)
    purchased_date = models.DateTimeField(auto_now=True)
    image_big = models.ImageField(upload_to="museum_packages")
    type = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    duration = models.CharField(max_length=20, null=True, blank=True)

    second_image = models.ImageField(upload_to="museum_packages")
    third_image = models.ImageField(upload_to="museum_packages")
    fourth_image = models.ImageField(upload_to="museum_packages")

    description = RichTextField()

    off_price = models.IntegerField(verbose_name="Enter the off price (USD)")
    adult_price = models.IntegerField(verbose_name="Enter the price for Adults (19-99) in USD")
    youth_price = models.IntegerField(verbose_name="Enter the price for Youths (6-18) in USD")
    infant_price = models.IntegerField(verbose_name="Enter the price for Infants (0-5) in USD")

    dates = models.ManyToManyField(Date)

    package_tag = models.IntegerField(editable=False)
    is_featured = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.package_tag:
            self.package_tag = random_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title or "Untitled Package"


class PurchasedTickets(models.Model):
    purchased_date = models.DateTimeField(auto_now=True)
    user = models.CharField(max_length=500, null=True, blank=True)
    package = models.CharField(max_length=1000, null=True, blank=True)
    total_price = models.IntegerField(default=0)

    adults = models.IntegerField(default=0)
    youths = models.IntegerField(default=0)
    infants = models.IntegerField(default=0)

    selected_date = models.CharField(max_length=20, null=True, blank=True)
    paid = models.BooleanField(default=False)

    package_tag = models.IntegerField(default=0)
    package_unique_identifier = models.IntegerField(default=0)

    qr_content = models.CharField(max_length=500, null=True, blank=True)

    qr_code = models.ImageField(upload_to="qr_codes", null=True, blank=True)
    qr_code_scanned = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.qr_content)
        canvas = Image.new('RGB', (398, 398), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)

        file_name = f"qr_code-{self.package_unique_identifier}.png"

        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(file_name, File(buffer), save=False)
        canvas.close()

        super().save(*args, **kwargs)

class Utilities(models.Model):
    privacy_policy = RichTextField()
    about_us = RichTextField()
    return_policy = RichTextField()
    refund_policy = RichTextField()
    terms_and_conditions = RichTextField()

class AgentProperties(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.IntegerField()



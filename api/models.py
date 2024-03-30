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

class BusPackages(models.Model):
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

    package_tag = models.IntegerField(default=random_number())

    def __str__(self):
        return str(self.title)



class Date(models.Model):
    date = models.DateField()

    def __str__(self):
        return str(self.date)


class MuseumPackages(models.Model):
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

    package_tag = models.IntegerField(default=random_number())

    def __str__(self):
        return str(self.title)


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
import random

from ckeditor.fields import RichTextField
from django.db import models


def random_number():
    return random.randint(10000,99999)

class HeroImage(models.Model):
    image = models.ImageField(upload_to="hero_images")

class BusPackages(models.Model):
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



class Date(models.Model):
    date = models.DateField()

    def __str__(self):
        return str(self.date)

    
class MuseumPackages(models.Model):
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

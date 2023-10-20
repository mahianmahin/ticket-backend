import random

from django.contrib import admin

from .models import *


@admin.register(HeroImage)
class HeroImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image']

@admin.register(BusPackages)
class BusPackageAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'duration', 'off_price', 'adult_price', 'youth_price', 'infant_price']

@admin.register(Date)
class DateAdmin(admin.ModelAdmin):
    list_display = ['id', 'date']

@admin.register(MuseumPackages)
class MuseumAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'duration', 'off_price', 'adult_price', 'youth_price', 'infant_price']
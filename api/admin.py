import random

from django.contrib import admin

from .models import *


@admin.register(HeroImage)
class HeroImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image']

@admin.register(BusPackages)
class BusPackageAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'package_tag', 'duration', 'off_price', 'adult_price', 'youth_price', 'infant_price', 'is_featured']

@admin.register(Date)
class DateAdmin(admin.ModelAdmin):
    list_display = ['id', 'date']

@admin.register(MuseumPackages)
class MuseumAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'duration', 'off_price', 'adult_price', 'youth_price', 'infant_price', 'is_featured']

@admin.register(PurchasedTickets)
class PurchasedAdmin(admin.ModelAdmin):
    list_display = ['purchased_date', 'user', 'package', 'selected_date', 'total_price', 'adults', 'youths', 'infants', 'paid', 'qr_code_scanned']

@admin.register(Utilities)
class UtilitiesAdmin(admin.ModelAdmin):
    list_display = ['privacy_policy', 'about_us', 'return_policy', 'refund_policy', 'terms_and_conditions']

@admin.register(AgentProperties)
class AgentPropertiesAdmin(admin.ModelAdmin):
    list_display = ['agent', 'code']

@admin.register(TicketFolders)
class FolderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'image']
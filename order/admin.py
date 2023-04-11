""" Registers the Purchase model in the admin interface. """

from django.contrib import admin
from order.models import Purchase


# Register your models here.
@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    """ This class describes the display of the Purchase on the admin panel"""
    pass

""" Registers the Hall, the Session and the Movie models in the admin interface. """

from django.contrib import admin
from .models import Session, Movie, Hall


# Register your models here.
@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    """ This class describes the display of the Hall on the admin panel"""
    pass


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """ This class describes the display of the Movie on the admin panel"""
    pass


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    """ This class describes the display of the Session on the admin panel"""
    pass

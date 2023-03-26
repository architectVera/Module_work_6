from django.contrib import admin
from .models import Session, Movie, Hall


# Register your models here.
@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    pass


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    pass


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    pass

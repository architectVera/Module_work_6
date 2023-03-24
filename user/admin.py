""" Registers the UserModel model in the admin interface. """


from django.contrib import admin
from .models import UserModel

# Register your models here.
admin.site.register(UserModel)

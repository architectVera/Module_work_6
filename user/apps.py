""" Configuration file for the user app  """

from django.apps import AppConfig


class UserConfig(AppConfig):
    """ Configuration file for the user app  """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

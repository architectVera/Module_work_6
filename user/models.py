""" Models for the user app  """

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserModel(AbstractUser):
    """A custom user model that extends the built-in `AbstractUser` class."""

    email = models.EmailField()
    wallet = models.DecimalField(decimal_places=2, default=10000.0, max_digits=10)

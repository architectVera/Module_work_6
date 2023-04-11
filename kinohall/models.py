""" Models for the kinohall app  """

import datetime

from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse


class Hall(models.Model):
    """A class representing a hall with a name and a number of seats"""

    name = models.CharField(max_length=100)
    seats = models.PositiveIntegerField(validators=[MinValueValidator(20), MaxValueValidator(250)])

    def __str__(self):
        """Returns the name of the hall as a string"""

        return str(self.name)

    def get_absolute_url(self):
        """Returns the absolute URL of the hall detail view"""

        return reverse('hall-detail', kwargs={'pk': self.pk})


class Movie(models.Model):
    """A class representing a movie with a title, description, year, and image"""

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    year = models.PositiveIntegerField(validators=[MaxValueValidator(2030)])
    image = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        """Returns the title of the movie as a string"""

        return str(self.title)

    def get_absolute_url(self):
        """Returns the absolute URL of the movie detail view"""

        return reverse('movie-detail', kwargs={'pk': self.pk})


class Session(models.Model):
    """A class representing a session with a start and end time, start
    and end date, price, hall, and movie"""

    start_time = models.TimeField()
    end_time = models.TimeField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        """Returns a string representation of the session"""

        return f"{self.movie} ({self.hall}): {self.start_date} {self.start_time}"

    def get_dates(self):
        """Returns a list of dates between the start and end date of the session"""

        delta = self.end_date - self.start_date
        dates = [str(self.start_date + datetime.timedelta(days=i)) for i in range(delta.days + 1)]
        return dates

    def get_absolute_url(self):
        """Returns the absolute URL of the session detail view"""

        return reverse('session-detail', kwargs={'pk': self.pk})

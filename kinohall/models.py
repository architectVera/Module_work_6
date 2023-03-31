import datetime

from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse


class Hall(models.Model):
    name = models.CharField(max_length=100)
    seats = models.PositiveIntegerField(validators=[MinValueValidator(20), MaxValueValidator(250)])

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """ This method return absolute url"""

        return reverse('hall-detail', kwargs={'pk': self.pk})


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    year = models.PositiveIntegerField(validators=[MaxValueValidator(2030)])
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """ This method return absolute url"""

        return reverse('movie-detail', kwargs={'pk': self.pk})


class Session(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.movie} ({self.hall}): {self.start_date} {self.start_time}"

    def get_dates(self):
        delta = self.end_date - self.start_date
        dates = [str(self.start_date + datetime.timedelta(days=i)) for i in range(delta.days + 1)]
        return dates

    def get_absolute_url(self):
        """ This method return absolute url"""

        return reverse('session-detail', kwargs={'pk': self.pk})


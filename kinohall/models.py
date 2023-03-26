from django.db import models
from django.urls import reverse


class Hall(models.Model):
    name = models.CharField(max_length=100)
    seats = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    year = models.PositiveIntegerField(max_length=4)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """ This method return absolute url"""

        return reverse('movie-detail', kwargs={'pk': self.pk})


class Session(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.movie} ({self.hall}): {self.date} {self.start_time}"
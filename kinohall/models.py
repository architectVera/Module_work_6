from django.db import models


class Hall(models.Model):
    name = models.CharField(max_length=100)
    seats = models.IntegerField()

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    year = models.IntegerField()

    def __str__(self):
        return self.title


class Session(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.movie} ({self.hall}): {self.date} {self.start_time}"
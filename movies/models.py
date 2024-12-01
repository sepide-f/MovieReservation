from django.conf import settings
from django.db import models


class movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class movieShowTimes(models.Model):
    salon = models.IntegerField()
    date = models.DateField(blank=False)
    showtime = models.TimeField(blank=False)
    movie = models.ForeignKey(movie, on_delete=models.CASCADE)

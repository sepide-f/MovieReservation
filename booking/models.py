from django.db import models
from movies.models import movieShowTimes
from users.models import CustomUser


class booking(models.Model):
    movie_showtime = models.ForeignKey(movieShowTimes, on_delete=models.CASCADE)
    seats = models.IntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

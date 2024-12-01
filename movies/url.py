from django.urls import path
from .views import manageMovies, addShowTimes, getShowTimes

urlpatterns = [
    path("movies/", manageMovies.as_view(), name='login'),
    path("showtimes/", addShowTimes.as_view(), name='login'),
    path("showtimes/<str:date>/", getShowTimes.as_view(), name='login'),
]

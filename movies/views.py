from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .decorators import role_required
from .models import movie, movieShowTimes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class manageMovies(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        movies = movie.objects.all()
        movies_data = [
            {
                "title": movie.title,
                "release_date": movie.description
            }
            for movie in movies
        ]
        return Response(movies_data, status=status.HTTP_200_OK)

    @role_required('Admin')
    def post(self, request):
        title = request.data.get("title")
        description = request.data.get("description")
        if not title or not description:
            return Response(
                {"error": "Title and Description are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        avoid_duplicate = movie.objects.filter(title=title)
        if avoid_duplicate:
            return Response(
                {"error": "movie already exists"},
                status=status.HTTP_409_CONFLICT
            )
        movies = movie.objects.create(title=title, description=description)
        return Response(
            {
                "message": "Movie added successfully.",
                "movie": {"title": movies.title, "description": movies.description},
            },
            status=status.HTTP_201_CREATED,
        )

    # @role_required
    # def put(self):

    @role_required('Admin')
    def delete(self, request, movie_id):
        movies = get_object_or_404(movie, id=movie_id)
        movies.delete()
        return Response({"message": "Movie deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class addShowTimes(APIView):
    permission_classes = [IsAuthenticated]

    @role_required('Admin')
    def post(self, request):
        movietitle = request.data.get("movie")
        Movie = get_object_or_404(movie, title=movietitle)
        date = request.data.get("date")
        showtime = request.data.get("showtime")
        salon = request.data.get("salon")
        if not date or not salon or not date or not showtime:
            return Response(
                {"error": "all the fields are necessary"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        movieshowtime = movieShowTimes.objects.filter(date=date, showtime=showtime, salon=salon)
        if movieshowtime:
            return Response({
                "message": "this salon is not available at this date and time"
            })
        try:
            movieShowTimes.objects.create(
                salon=salon,
                date=date,
                movie=Movie,
                showtime=showtime
            )

            return Response(
                {
                    "message": "Movie added successfully.",
                    "movie": {"id": movieshowtime.date, "title": movieshowtime.showtime,
                              "description": movieshowtime.salon},
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class getShowTimes(APIView):
    def get(self, request, date):
        show_times = get_object_or_404(movieShowTimes, date=date)
        return Response({
            "movie": show_times.movie.title, "showtime": show_times.showtime
        }, status=status.HTTP_200_OK)


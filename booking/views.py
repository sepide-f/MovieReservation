from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import booking
from rest_framework.views import Response
from django.shortcuts import get_object_or_404
from .models import movieShowTimes
from movies.decorators import role_required


class AvailableSeats(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, showtime_id):
        seats = booking.objects.filter(movie_showtime=showtime_id)


class UserGetReservations(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        bookings = booking.objects.get(user=user)
        if not bookings:
            return Response({
                "message": "there is no reservation for this user"
            }, status=status.HTTP_404_NOT_FOUND)
        booking_data = [
            {
                "seat": bookings.seat,
                "release_date": bookings.movie_showtime
            }
            for book in bookings]
        return Response(booking_data, status=status.HTTP_200_OK)


class UserDeleteAddReservation(APIView):
    permission_class = [IsAuthenticated]

    def post(self, request, showtime_id, seat):
        user = request.user
        Movie_showtime = movieShowTimes.objects.get(id=showtime_id)
        check_duplicate = booking.objects.filter(seats=seat, movie_showtime=Movie_showtime)
        if check_duplicate:
            return Response({
                "message": "this seat is not available at this date and time"
            })
        Booking = booking.objects.create(user=user, movie_showtime=Movie_showtime, seats=seat)
        return Response(
            {
                "message": "Reservation added successfully.",
                "booking": {
                    "user_id": Booking.user.username,
                    "movie_showtime": {
                        "salon": Booking.movie_showtime.salon,
                        "date": str(Booking.movie_showtime.date),
                        "showtime": str(Booking.movie_showtime.showtime),
                        "movie": Booking.movie_showtime.movie.title,  # Access movie title
                    },
                    "seats": Booking.seats,
                },
            },
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, showtime_id, seat):
        user = request.user
        bookings = booking.objects.filter(user=user, movie_showtime_id=showtime_id, seats=seat)
        if bookings.exists():
            bookings.delete()
            return Response({"message": "All matching reservations deleted successfully."},
                            status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "No matching reservations found."}, status=status.HTTP_404_NOT_FOUND)


class AdminGetReservations(APIView):
    permission_classes = [IsAuthenticated]

    @role_required("Admin")
    def get(self, request):
        Reservation = booking.objects.all()
        movies_data = [
            {
                "seats": reservation.seats,
                "user_name": reservation.user.username,
                "movie_showtime": {
                    "salon": reservation.movie_showtime.salon,
                    "date": reservation.movie_showtime.date,
                    "showtime": reservation.movie_showtime.showtime,
                    "movie": reservation.movie_showtime.movie.title,
                },
            }
            for reservation in Reservation
        ]
        return Response(movies_data, status=status.HTTP_200_OK)

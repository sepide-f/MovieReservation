from django.urls import path
from .views import AvailableSeats, UserGetReservations, AdminGetReservations, UserDeleteAddReservation

urlpatterns = [
    path("/<int:showtime_id>", AvailableSeats.as_view(), name='login'),
    path("user/reservations/", UserGetReservations.as_view(), name='login'),
    path("user/reservation/<int:showtime_id>/<int:seat>", UserDeleteAddReservation.as_view(), name='login'),
    path("Admin/all/reservation/", AdminGetReservations.as_view(), name='login'),
]

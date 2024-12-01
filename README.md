# Movie Reservation System 🎥

## Overview
The **Movie Reservation System** is a backend service for managing movie reservations. It provides authentication, movie and showtime management, seat reservations, and reporting features.

## Features
- **User Authentication**: Sign up, log in, and role-based access control (Admin and Regular User).
- **Movie Management**: Add, update, delete movies, and schedule showtimes (Admins only).
- **Reservations**: Reserve seats, check availability of seats, manage seat reservations.

## Technology Stack
- **Backend Framework**: Django
- **Database**: sqlite3
- **Authentication**: Token-Based Authentication

## Installation
1. Clone the repository:  
   `git clone https://github.com/sepide-f/MovieReservation.git`
2. Set up a virtual environment and install dependencies:  
   `pip install -r requirements.txt`
3. Configure the database in `settings.py`.
4. Apply migrations:  
   `python manage.py migrate`
5. Run the server:  
   `python manage.py runserver`

## API Endpoints
- **Authentication**: `/signup/`, `/login/`
- **Movie Management**: `/movies/`
- **Showtime Management**: `/showtimes/`, `/showtimes/<date>/`
- **Reservations**: `user/reservation/<int:showtime_id>/<int:seat>`, `user/reservations/`, `Admin/all/reservation/`, `/<int:showtime_id>/`

## Future Enhancements
- Add serializer.
- Implement email notifications.
- Introduce multi-language support.
- Implement Postgres



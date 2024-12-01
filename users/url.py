from django.urls import path
from .views import LoginView, RegisterView, UserRole

urlpatterns = [
    path("login/", LoginView.as_view(), name='login'),
    path("register/", RegisterView.as_view(), name='register'),
    path("role/",  UserRole.as_view(), name='role'),
]

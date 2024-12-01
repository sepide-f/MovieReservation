from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from .models import CustomUser, Role
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return JsonResponse(
                {'error': 'Username and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = authenticate(
            username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return JsonResponse(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }
            )
        else:
            return JsonResponse(
                {'error': 'Invalid username or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = CustomUser.objects.create_user(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            refresh = RefreshToken.for_user(user)
            return JsonResponse(
                {'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRole(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_role = Role.objects.get(user=request.user)
            return JsonResponse(
                {
                    "role": user_role.name
                }
            )
        except Role.DoesNotExist:
            return JsonResponse(
                {
                    'error': 'user role doesnt exist'
                }
            )

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from .models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')

        if not username or not password:
            return Response({'message': 'Username and password are required'}, status=400)
        if User.objects.filter(username=username).exists():
            return Response({'message': 'Username already exists'}, status=400)
        if email and User.objects.filter(email=email).exists():
            return Response({'message': 'Email already exists'}, status=400)
        user = User.objects.create_user(username=username, password=password, email=email)
        return Response({'message': 'User created successfully'}, status=201)

        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'User created successfully',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=201)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Login successful',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=200)
        else:
            return Response({'message': 'Invalid credentials'}, status=401)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logout successful'}, status=200)
        except TokenError:
            return Response({'message': 'Invalid refresh token'}, status=400)

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'Protected view'}, status=200)
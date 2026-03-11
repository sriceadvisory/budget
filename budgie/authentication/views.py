from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.shortcuts import render

from .models import User


def index(request):
    return render(request, 'budgie/index.html')


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')

        if not username or not password:
            return Response(
                {'error': 'Username and password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Username already exists.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if email and User.objects.filter(email=email).exists():
            return Response(
                {'error': 'Email already exists.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(username=username, password=password, email=email)
        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'User created successfully.',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        identifier = request.data.get('username')
        password = request.data.get('password')

        if not identifier or not password:
            return Response(
                {'error': 'Username / email and password are required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        UserModel = get_user_model()

        # Allow login by either username or email.
        base_qs = UserModel.objects.all()
        user_obj = base_qs.filter(username=identifier).first()
        if user_obj is None:
            user_obj = base_qs.filter(email__iexact=identifier).first()

        user = None
        if user_obj is not None:
            raw_stored = user_obj.password or ""

            # Case 1: normal Django-hashed password (has algorithm prefix, e.g. "pbkdf2_sha256$")
            if "$" in raw_stored:
                if check_password(password, raw_stored):
                    user = user_obj

            # Case 2: legacy/plain-text password saved directly via admin/model (no "$" prefix)
            else:
                if password == raw_stored:
                    # Treat as valid, then immediately rehash and save securely.
                    user_obj.set_password(password)
                    user_obj.save(update_fields=["password"])
                    user = user_obj

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Login successful.',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response(
            {'error': 'Invalid credentials.'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logout successful.'}, status=status.HTTP_200_OK)
        except TokenError:
            return Response(
                {'error': 'Invalid or expired refresh token.'},
                status=status.HTTP_400_BAD_REQUEST
            )